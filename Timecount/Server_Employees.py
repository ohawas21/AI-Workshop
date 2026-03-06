import json
import os
import httpx
from fastmcp import FastMCP

BASE_URL = "https://tutorial.formatgold.de/api"
API_TOKEN = os.environ.get("API_TOKEN", "2b5fe67c2d8ac17bed27720a76d10584050b07be99028a31feb98c874fbff64a").strip()

def load_openapi_spec() -> dict:
    here = os.path.dirname(__file__)
    with open(os.path.join(here, "Employee_schema_3.0.json"), "r", encoding="utf-8") as f:
        return json.load(f)

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
    mcp.run(transport="stdio")