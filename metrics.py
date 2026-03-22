from prometheus_client import start_http_server, Counter, Summary, Gauge

# LLM metrics
llm_latency = Summary('llm_latency_seconds', 'LLM response latency')
llm_requests = Counter('llm_requests_total', 'Total LLM requests')
llm_errors = Counter('llm_errors_total', 'Total LLM errors')

# RAG metrics
rag_latency = Summary('rag_latency_seconds', 'RAG retrieval latency')
rag_docs = Gauge('rag_docs_retrieved', 'Number of docs retrieved')

# Agent metrics
agent_steps = Counter(
    'agent_steps_total',
    'Total agent steps',
    ['node_name']
)

node_latency = Summary(
    'agent_node_latency_seconds',
    'Latency per node',
    ['node_name']
)

def start_metrics_server():
    start_http_server(8000)
    