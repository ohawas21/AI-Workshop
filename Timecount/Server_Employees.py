import json
import os
import socket
import time
import signal
import subprocess
import httpx
from fastmcp import FastMCP

BASE_URL = "https://tutorial.formatgold.de/api"
API_TOKEN = os.environ.get("API_TOKEN", "2b5fe67c2d8ac17bed27720a76d10584050b07be99028a31feb98c874fbff64a").strip()

def load_openapi_spec() -> dict:
    here = os.path.dirname(__file__)
    with open(os.path.join(here, "Employee_schema_3.0.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def free_port(port: int, timeout: float = 3.0):
    try:
        result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        for pid in result.stdout.strip().split("\n"):
            if pid.strip():
                os.kill(int(pid.strip()), signal.SIGTERM)
    except Exception:
        pass
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return
        time.sleep(0.1)

client = httpx.AsyncClient(
    base_url=BASE_URL,
    headers={"Authorization": f"Bearer {API_TOKEN}"},
    timeout=30.0,
)

openapi_spec = load_openapi_spec()

mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="Employees"
)

if __name__ == "__main__":
    free_port(8001)
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        pass
