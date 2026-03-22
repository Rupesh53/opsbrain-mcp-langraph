# 📊 OpsBrain MCP LangGraph – Monitoring Setup (Netdata)

This section explains how to enable **real-time monitoring** for your AI agent using Netdata.

---

## 🚀 Overview

We are monitoring:

* 🤖 LLM metrics (latency, requests, errors)
* 🔁 Agent execution steps
* 📡 Prometheus-style `/metrics` endpoint

---

## 🧠 Architecture

```
OpsBrain Agent (port 8000)
        ↓
/metrics endpoint
        ↓
Netdata (port 19999)
        ↓
Dashboard (UI)
```

---

## 📁 Prerequisites

* Docker installed
* Kubernetes kubeconfig available
* `prometheus.conf` file created

---

## 📄 Step 1: Create Netdata Config

Create a file named `prometheus.conf`:

```yaml
jobs:
  - name: opsbrain_ai
    url: http://opsbrain-ai-app:8000/metrics
```

---

## 🐳 Step 2: Create Docker Network

```bash
docker network create opsbrain-net
```

---

## 🤖 Step 3: Run OpsBrain Agent Container

```bash
docker run -d \
  --name opsbrain-ai-app \
  -p 8000:8000 \
  --add-host=host.docker.internal:host-gateway \
  -v "C:\Users\hp Elitebook 840 g5\.kube:/root/.kube" \
  --network opsbrain-net \
  opsbrain-agent
```

---

## 📊 Step 4: Run Netdata Container

```bash
docker run -d \
  --name netdata \
  --network opsbrain-net \
  -p 19999:19999 \
  -v "C:\Users\hp Elitebook 840 g5\AIworkspace\opsbrain-mcp-langraph\prometheus.conf:/etc/netdata/go.d/prometheus.conf" \
  netdata/netdata
```

---

## 🔍 Step 5: Verify Metrics Endpoint

From host:

```bash
curl http://localhost:8000/metrics
```

From Netdata container:

```bash
docker exec netdata curl http://opsbrain-ai-app:8000/metrics
```

---

## 🌐 Step 6: Open Netdata Dashboard

```
http://localhost:19999
```

---

## 🔎 Step 7: Search Metrics

Use the search bar and look for:

* `llm_latency_seconds`
* `llm_requests_total`
* `llm_errors_total`
* `agent_steps_total`

---

## ⚠️ Common Issues & Fixes

### ❌ Metrics not visible

* Ensure agent has executed at least once
* Restart Netdata:

  ```bash
  docker restart netdata
  ```

---

### ❌ Cannot resolve `opsbrain-ai-app`

* Ensure both containers are in same network:

  ```bash
  docker network inspect opsbrain-net
  ```

---

### ❌ YAML parsing issues

* Ensure no Windows CRLF issues:

  ```bash
  dos2unix prometheus.conf
  ```

---

### ❌ kubeconfig not working

* Ensure mount path is correct:

  ```bash
  -v "C:\Users\<user>\.kube:/root/.kube"
  ```

---

## 🎯 Result

You now have:

* ✅ AI Agent (LangGraph)
* ✅ Prometheus Metrics
* ✅ Netdata Monitoring Dashboard
* ✅ Real-time Observability

---

## 🚀 Next Steps

* Add Grafana dashboards
* Configure alerts (LLM latency, failures)
* Convert setup to `docker-compose`

---
