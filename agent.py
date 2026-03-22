from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_community.llms import Ollama
from metrics import start_metrics_server, llm_latency, llm_requests, llm_errors, agent_steps,node_latency



# 🔧 Import tools directly (no HTTP MCP)
from mcp_server import get_pods, check_dns, check_egress, network_policy, cleanup

# ------------------------
# STATE
# ------------------------
class State(TypedDict):
    query: str
    tool_output: str
    analysis: str
    fix: str

# ✅ Use lightweight model
# llm = Ollama(model="phi")   # if running in local and no dockerfile
llm = Ollama(
    model="phi",
    base_url="http://host.docker.internal:11434"
)

# ------------------------
# 🧠 AGENT 1: TOOL SELECTOR
# ------------------------
def tool_selector(state: State):
    print("\n[Agent] Selecting tool...")
    agent_steps.labels(node_name="tool").inc()

    with node_latency.labels("tool").time(): 
        query = state["query"].lower()

        if "dns" in query:
            output = check_dns()
        elif "internet" in query or "egress" in query:
            output = check_egress()
        elif "policy" in query:
            output = network_policy()
        else:
            output = get_pods()

        print("\n[DEBUG TOOL OUTPUT]\n", output)  # 🔥 Debug visibility

        return {"tool_output": output}


# ------------------------
# 🧠 AGENT 2: ANALYZER
# ------------------------
def analyzer(state: State):
    print("\n[Agent] Analyzing issue...")
    agent_steps.labels(node_name="analyze").inc()   
    with node_latency.labels("analyze").time():
        prompt = f"""
    You are a Kubernetes networking expert.

    Analyze the issue using the tool output.

    Rules:
    - Always give a clear answer
    - Do NOT say "I cannot help"
    - If tool output has error → say "Tool execution failed"
    - Be concise and practical

    Return format:

    Issue:
    <what is wrong>

    Reason:
    <why it is happening>

    User Query:
    {state['query']}

    Tool Output:
    {state['tool_output']}
    """
        
        analysis = call_llm(prompt)

        print("\n[DEBUG ANALYSIS]\n", analysis)

        return {"analysis": analysis}


# ------------------------
# 🛠 AGENT 3: FIXER
# ------------------------
def fixer(state: State):
    print("\n[Agent] Suggesting fix...")
    agent_steps.labels(node_name="fix").inc()
    
    
    with node_latency.labels("fix").time():
        prompt = f"""
    You are a Kubernetes SRE expert.

    Based on the issue below, provide a fix.

    Rules:
    - Give exact kubectl commands
    - Be practical
    - Do NOT say "I cannot help"

    Issue:
    {state['analysis']}

    Return format:

    Fix:
    <steps + commands>
    """

        fix = call_llm(prompt)

        return {"fix": fix}


# ------------------------
# BUILD GRAPH
# ------------------------
builder = StateGraph(State)

builder.add_node("tool", tool_selector)
builder.add_node("analyze", analyzer)
builder.add_node("fix", fixer)

builder.set_entry_point("tool")

builder.add_edge("tool", "analyze")
builder.add_edge("analyze", "fix")
builder.add_edge("fix", END)

graph = builder.compile()




@llm_latency.time()
def call_llm(prompt):
    llm_requests.inc()
    try:
        response = llm.invoke(prompt)   # your existing call
        return response
    except Exception:
        llm_errors.inc()
        raise
# ------------------------
# RUN
# ------------------------
if __name__ == "__main__":
    start_metrics_server()
    # 🔥 Change your test query here
    query = "Pods cannot access internet"

    result = graph.invoke({
        "query": query
    })

    print("\n==============================")
    print("🧠 FINAL ANALYSIS:\n", result["analysis"])
    print("\n🛠 FINAL FIX:\n", result["fix"])
    print("==============================\n")
   
    # 🧹 Cleanup test pods (optional)
    cleanup()