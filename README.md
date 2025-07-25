# AI Agents Experiments For ChatOps

This repository is my experimentation on ai-agents that are focussed on DevOps related tasks, basically ChatOps concept.
The motivation is to make life easier for anyone - experienced or novice alike, to be able to interact with the 
Kubernetes/Cloud etc., using natural language instructions. Currently, I am sharing agent for Kubernetes related tasks.

Although the API responses may not be great in terms of formatting - specially when trying to get info, but it prints the
commands and output of those command in the console logs which may be more useful in those cases. Works fine when it 
comes to executing instruction that acts on the resources - creating pods, deployments, services or scaling up/down etc.

I am using agno(formerly phidata) framework for creating the agents which I found simple to use. Here are couple of
relevant documentation references -
1. Agents Team - https://docs.agno.com/agents/teams
2. Python function - https://docs.agno.com/tools/functions

Do try it out and have fun!

Happy Learning!


### Prerequisite

1. Local or Remote Kubernetes cluster setup. For local you can use Podman/Kind. More details [here](https://podman-desktop.io/blog/running-a-local-kubernetes-cluster-with-podman-desktop).

2. `kubectl` installed and the terminal where you plan to run the python code is able to successfully run the `kubectl` commands without error. Example command - `kubectl get pods`.

### Dependencies

Run the following command in the terminal to install the dependencies.
```
pip install python-dotenv agno openai fastapi pydantic uvicorn
```

Also, add a `.env` file at the root of the folder with your OpenAI API/Groq API key(code currently supports these two). The entries will look like this:

```
OPENAI_API_KEY=
GROQ_API_KEY=
```

Groq is free. You can get the Groq API key from [here](https://console.groq.com/keys) - Login will be needed.

### Running the Code

Run the file - `K8DevopsAgentWithApi.py`

Use `Postman` or any other tool to hit the following endpoint:

```
POST http://localhost:8000/execute_k8s_instruction
```
Body(raw/json) :
```
{
    "instruction": "Create a pod with image nginx"
}
```

Other examples of instructions:

```
{
    "instruction": "Get the names of pods in all namespaces"
}
```
```
{
    "instruction": "Create a deployment with name mydeploy from image nginx"
}
```
```
{
    "instruction": "Scale up the deployment mydeploy to 3 pods"
}
```
```
{
    "instruction": "Scale down the deployment mydeploy to 1 pod"
}
```
