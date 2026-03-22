from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP("k8s-network-tools")

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

# ------------------------
# TOOL: GET PODS
# ------------------------
@mcp.tool()
def get_pods():
    return run_cmd("kubectl get pods -A -o wide")

# ------------------------
# TOOL: DNS CHECK (FIXED)
# ------------------------
@mcp.tool()
def check_dns():
    cmd = (
        "kubectl run dns-test --image=busybox --restart=Never "
        "-- nslookup kubernetes.default"
    )
    return run_cmd(cmd)

# ------------------------
# TOOL: INTERNET CHECK (FIXED)
# ------------------------
@mcp.tool()
def check_egress():
    cmd = (
        "kubectl run net-test --image=busybox --restart=Never "
        "-- wget -qO- http://google.com"
    )
    return run_cmd(cmd)

# ------------------------
# TOOL: NETWORK POLICY
# ------------------------
@mcp.tool()
def network_policy():
    return run_cmd("kubectl get networkpolicy -A")

# ------------------------
# TOOL: CLEANUP TEST PODS
# ------------------------
@mcp.tool()
def cleanup():
    return run_cmd("kubectl delete pod dns-test net-test --ignore-not-found")

# ------------------------
# RUN
# ------------------------
if __name__ == "__main__":
    mcp.run()  # stdio mode (correct for your MCP version)