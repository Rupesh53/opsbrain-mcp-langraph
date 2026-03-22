# 🚀 Kubernetes AI Network Troubleshooting Agent

An **Agentic AI system** that automatically diagnoses Kubernetes network issues using **LangGraph + Local LLM + MCP-style tools**.

This project simulates an **AI SRE (Site Reliability Engineer)** that:

* Runs real `kubectl` commands
* Analyzes cluster/network issues
* Suggests actionable fixes

---

## 🧠 Architecture Overview

The system is built using a **multi-agent workflow**:

1. **Tool Agent (Inspector)**

   * Executes Kubernetes commands (`kubectl`)
   * Collects cluster/network data

2. **Analyzer Agent (AI Brain)**

   * Uses a local LLM (Ollama)
   * Identifies root cause of issues

3. **Fix Agent (SRE Assistant)**

   * Suggests exact fixes
   * Provides `kubectl` commands

---

## 🧩 Tech Stack

* **LangGraph** → Agent orchestration
* **Ollama** → Local LLM runtime
* **Python** → Core logic
* **Kubernetes (Docker Desktop / AKS)** → Target environment
* **MCP-style tools** → Tool abstraction layer

---

## 📁 Project Structure

```
k8s-ai-agent/
│
├── agent.py          # LangGraph multi-agent workflow
├── mcp_server.py     # Tool definitions (kubectl commands)
├── requirements.txt
└── README.md
```

---

## ⚙️ Prerequisites

* Python 3.9+
* `kubectl` configured (Docker Desktop Kubernetes or AKS)
* Ollama installed

---

## 📦 Installation

```bash
git clone <your-repo-url>
cd k8s-ai-agent

pip install -r requirements.txt
```

---

## 🤖 Setup Local LLM

Install a lightweight model (recommended for low RAM):

```bash
ollama pull phi
```

Update model in `agent.py`:

```python
llm = Ollama(model="phi")
```

---

## ▶️ Run the Project

```bash
python agent.py
```

---

## 🧪 Example Queries

Edit inside `agent.py`:

```python
query = "Pods cannot access internet"
```

Try:

* `DNS not working`
* `Check network policies`
* `Why pods are failing`

---

## 🔍 What Happens Internally

```
User Query
   ↓
Tool Agent (kubectl execution)
   ↓
Analyzer Agent (LLM reasoning)
   ↓
Fix Agent (solution generation)
   ↓
Final Output
```

---

## 🧠 Example Output

```
ANALYSIS:
Issue: DNS resolution failure
Reason: nslookup failed inside pod

FIX:
kubectl get pods -n kube-system
kubectl logs -l k8s-app=kube-dns -n kube-system
```

---

## ⚠️ Notes

* Works best with a running Kubernetes cluster
* Docker Desktop Kubernetes is supported
* No Azure-specific networking (NSG/UDR) in local setup

---

## 🔥 Future Enhancements

* ✅ LLM-based dynamic tool selection (no if-else)
* ✅ Auto-healing (execute fixes automatically)
* ✅ Azure AKS integration (NSG, route tables)
* ✅ UI dashboard (React + API)
* ✅ Observability integration (Prometheus/Grafana)

---

## 💡 Use Case

This project demonstrates how to build:

👉 **AI-powered DevOps / SRE assistant**
👉 **Agentic troubleshooting systems**
👉 **Tool-augmented LLM workflows**

---

## 🧑‍💻 Author

Built by Rupesh Nayak
DevOps | Kubernetes | AI Systems

---

## ⭐ If you like this project

Give it a star ⭐ and share your feedback!
