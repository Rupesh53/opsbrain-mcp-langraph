from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_community.llms import Ollama

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
llm = Ollama(model="phi")   # change to mistral if RAM allows

# ------------------------
# 🧠 AGENT 1: TOOL SELECTOR
# ------------------------
def tool_selector(state: State):
    print("\n[Agent] Selecting tool...")

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

    analysis = llm.invoke(prompt)

    print("\n[DEBUG ANALYSIS]\n", analysis)

    return {"analysis": analysis}


# ------------------------
# 🛠 AGENT 3: FIXER
# ------------------------
def fixer(state: State):
    print("\n[Agent] Suggesting fix...")

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

    fix = llm.invoke(prompt)

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


# ------------------------
# RUN
# ------------------------
if __name__ == "__main__":

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