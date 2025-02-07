# AI Agents Experiments For ChatOps

###Prerequisite

1. Local or Remote Kubernetes cluster setup. For local you can use Podman. More details [here](https://podman-desktop.io/blog/running-a-local-kubernetes-cluster-with-podman-desktop).

2. `kubectl` installed and the terminal where you plan to run the python code is able to successfully run the `kubectl` commands without error. Example command - `kubectl get pods`.

### Dependencies

Run the following command in the terminal to install the dependencies.
```
pip install python-dotenv agno openai fastapi pydantic uvicorn
```

Also, add a `.env` file at the root of the folder with your OpenAI API key(or any other provider of your choice). The entries will look like this:

```
OPENAI_API_KEY=
```

### Running the Code
Run the file - `K8DevopsAgentWithApi.py`

Use Postman or any other tool to hit the following endpoint:

```
POST http://localhost:8000/execute_k8s_instruction
```
Body(raw/json) :
```
{
    "instruction": "Create a pod with image nginx"
}
```
