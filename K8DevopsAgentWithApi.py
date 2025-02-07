import os
import subprocess
from dotenv import load_dotenv
from agno.agent import Agent
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()

# Get API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Initialize FastAPI app
app = FastAPI()

class InstructionRequest(BaseModel):
    instruction: str

# Function to query LLM for Kubernetes command generation
def get_k8s_command_from_llm(instruction):
    print(f"Instruction received: {instruction}")
    prompt = f"Generate the Kubernetes CLI command for the following instruction: '{instruction}'. NO PREAMBLE, NO MARKDOWN."

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a Kubernetes CLI expert."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Function to execute kubectl command using subprocess
def execute_kubectl_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

class LLMCommandAgent(Agent):
    """Fetches the corresponding Kubernetes command from LLM."""

    def run(self, context):
        instruction = context.get("instruction", "")

        if instruction:
            command = get_k8s_command_from_llm(instruction)
            context["command"] = command
            print(f"[LLMCommandAgent] Generated command: {command}")
        else:
            print("[LLMCommandAgent] No instruction found.")

class CommandExecutorAgent(Agent):
    """Executes the Kubernetes command received from LLM."""

    def run(self, context):
        command = context.get("command")

        if command:
            print(f"[CommandExecutorAgent] Executing command: {command}")
            success, output = execute_kubectl_command(command)

            if success:
                print(f"[CommandExecutorAgent] Command executed successfully:\n{output}")
                return output
            else:
                print(f"[CommandExecutorAgent] Command execution failed:\n{output}")
                raise HTTPException(status_code=500, detail=output)
        else:
            print("[CommandExecutorAgent] No command to execute.")
            raise HTTPException(status_code=400, detail="No command generated.")

@app.post("/execute_k8s_instruction")
def execute_instruction(request: InstructionRequest):
    """API endpoint to process Kubernetes instructions."""
    context = {"instruction": request.instruction}

    # Create and run agents
    agents = [
        LLMCommandAgent(name="LLMCommandGenerator"),
        CommandExecutorAgent(name="CommandExecutor"),
    ]

    for agent in agents:
        output = agent.run(context)

    return {"message": "Command executed successfully", "output": output}

# Run FastAPI with Uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
