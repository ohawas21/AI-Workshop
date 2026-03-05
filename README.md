# 🌤️ Building Your First MCP Server — Weather Workshop

A hands-on workshop project that teaches you how to build a custom **Model Context Protocol (MCP)** server from scratch. By the end, you'll have a working weather tool that Claude can call in real-time.

---

## 📚 What is MCP?

**Model Context Protocol (MCP)** is an open standard that lets AI models like Claude connect to external tools and data sources. Think of it as a USB-C port for AI — a universal way to plug in any capability you want.

Without MCP → Claude can only use its training knowledge  
With MCP → Claude can call your code, your APIs, your databases

---

## 🗂️ Project Structure

```
weather/
├── weather.py          # The MCP server — this is what you'll build
├── pyproject.toml      # Python project config & dependencies
└── .venv/              # Auto-created virtual environment (by uv)
```

---

## ✅ Prerequisites

Before starting, make sure you have the following installed:

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.10+ | Runtime | [python.org](https://python.org) |
| `uv` | Fast Python package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Claude Desktop | The AI client | [claude.ai/download](https://claude.ai/download) |

### Verify your setup
```bash
python3 --version    # Should be 3.10 or higher
which uv             # Should return a path like /Users/yourname/.local/bin/uv
```

---

### 🆘 Don't have Python or uv yet? Start here.

#### 1. Install Python 3.13 (recommended)

**Mac:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click **"Download Python 3.13.x"** (the big yellow button)
3. Open the downloaded `.pkg` file and follow the installer
4. Once done, open a **new** Terminal window and verify:
   ```bash
   python3 --version
   # Expected: Python 3.13.x
   ```

**Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download and run the installer
3. ⚠️ **Important:** On the first screen, check **"Add Python to PATH"** before clicking Install
4. Open Command Prompt and verify:
   ```bash
   python --version
   # Expected: Python 3.13.x
   ```

---

#### 2. Install `uv`

**Mac / Linux** — run this in Terminal:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then reload your terminal so it picks up the new command:
```bash
source ~/.zshrc
```

**Windows** — run this in PowerShell:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then close and reopen PowerShell.

---

#### 3. Verify both are working
```bash
python3 --version    # Should print Python 3.10 or higher
which uv             # Mac/Linux: should print a path
uv --version         # All platforms: should print uv x.x.x
```

If `which uv` still returns nothing after installing, close your terminal completely and open a fresh one — it needs to reload your PATH.

---

---

## 🚀 Getting Started

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Workshop-Custom-MCP-Trial-Weather-.git
cd AI-Workshop-Custom-MCP-Trial-Weather-/weather
```

### Step 2 — Run the server once to install dependencies

This step creates the virtual environment and downloads all required packages. Only needed the first time.

```bash
/Users/YOUR_USERNAME/.local/bin/uv run weather.py
```

> ⚠️ Replace `YOUR_USERNAME` with your actual macOS username.  
> You'll see `Installed X packages` — that means it worked!

### Step 3 — Connect to Claude Desktop

Open your Claude Desktop config file:

```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Add the weather server under `mcpServers`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/YOUR_USERNAME/AI-Workshop-Custom-MCP-Trial-Weather-/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

> ⚠️ Use the **full absolute path** to `uv` (not just `uv`). Claude Desktop runs with a limited PATH and won't find it otherwise.  
> Find your full path with: `which uv`

### Step 4 — Restart Claude Desktop

Fully quit Claude (⌘Q) and reopen it. You should now see the weather tool available.

---

## 🔍 How the MCP Server Works

Here's the anatomy of `weather.py`:

```python
from mcp.server.fastmcp import FastMCP

# 1. Create the server
mcp = FastMCP("weather")

# 2. Define a tool using a decorator
@mcp.tool()
async def get_forecast(city: str) -> str:
    """Get the weather forecast for a city."""
    # Your logic here — call an API, return a string
    ...

# 3. Run it
if __name__ == "__main__":
    mcp.run()
```

That's it. The `@mcp.tool()` decorator is all Claude needs to discover and call your function.

---

## 🛠️ Build Your Own MCP Tool — Step by Step

### 1. Create your project folder
```bash
mkdir my-mcp-server && cd my-mcp-server
```

### 2. Create `pyproject.toml`
```toml
[project]
name = "my-mcp-server"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "mcp[cli]>=1.0.0",
    "httpx>=0.27.0"
]
```

### 3. Create your server file `server.py`
```python
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("my-tool")

@mcp.tool()
async def my_tool(input: str) -> str:
    """Describe what your tool does — Claude reads this description."""
    return f"You said: {input}"

if __name__ == "__main__":
    mcp.run()
```

### 4. Test it
```bash
uv run server.py
```

### 5. Register it in Claude Desktop's config
```json
{
  "mcpServers": {
    "my-tool": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": ["--directory", "/path/to/my-mcp-server", "run", "server.py"]
    }
  }
}
```

---

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed to spawn process: No such file or directory` | `uv` not found or wrong path | Use full absolute path from `which uv` |
| `uv not found` | `uv` is not installed | Run the install curl command above |
| `Request timed out` | First-run dependency download is slow | Run `uv run weather.py` manually first in terminal |
| `VIRTUAL_ENV does not match` warning | Outer venv conflicts with project venv | Harmless — safely ignore it |
| Config changes not taking effect | Claude wasn't fully restarted | Quit with ⌘Q, not just closing the window |

---

## 📖 Further Reading

- [MCP Official Documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Debugging Guide](https://modelcontextprotocol.io/docs/tools/debugging)
- [uv Documentation](https://docs.astral.sh/uv/)

---

## 💡 Ideas for Your Own MCP Server

Once you've got weather working, try building one of these:

- 📅 **Calendar tool** — Read/write Google Calendar events
- 🗄️ **Database tool** — Query a local SQLite database
- 📁 **File tool** — Read and summarize local documents
- 🔎 **Search tool** — Wrap any REST API (news, stocks, sports)
- 🏠 **Home automation** — Control smart home devices

---

## 🤝 Contributing

Built something cool? Open a PR and share it with the workshop community!

---

*Made with ❤️ for the AI Workshop*
