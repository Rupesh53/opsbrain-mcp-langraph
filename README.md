# Kubernetes AI Agent (Local)

## Setup

```bash
pip install -r requirements.txt
ollama run llama3
```

## Run MCP Server

```bash
python mcp_server.py
```

## Run Agent

```bash
python agent.py
```

## Test Queries

- Pods cannot access internet
- DNS not working in cluster
- Check network policies
