# 🌤️ MCP Workshop — Hackathon Setup Guide

Get your MCP servers running in Claude Desktop. This guide covers three servers: **Weather**, **Gmail**, and **Custom (FastMCP)**.

---

## ✅ Prerequisites — Install These First

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.10+ | Runtime | [python.org](https://python.org) |
| `uv` | Python package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Claude Desktop | The AI client | [claude.ai/download](https://claude.ai/download) |

**Verify your setup:**
```bash
python3 --version   # Should be 3.10 or higher
uv --version        # Should print uv x.x.x
```

> **Don't have Python or uv?** See the [install guides](#-installing-python--uv) at the bottom of this file.

---

## 📦 Project Structure

```
AI-Workshop/
├── weather/
│   └── weather.py
├── gmail/
│   └── (gmail MCP files)
└── custom-mcp/
    └── server.py
```

---

---

# ☁️ MCP 1 — Weather Server

A simple MCP that lets Claude fetch real-time weather data.

### Step 1 — Navigate to the project folder

```bash
cd AI-Workshop/weather
```

### Step 2 — Create a virtual environment

```bash
uv venv
```

### Step 3 — Install dependencies

```bash
uv pip install httpx
uv pip install mcp
```

### Step 4 — Run the server once to verify it works

```bash
uv run weather.py
```

You should see the server start without errors.

### Step 5 — Add to Claude Desktop config

Open the config file:
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Add the following inside `mcpServers`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/YOUR_USERNAME/AI-Workshop/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

> ⚠️ Replace `YOUR_USERNAME` with your actual username. Find the full `uv` path with: `which uv`

### Step 6 — Restart Claude Desktop

Fully quit Claude (**⌘Q**) and reopen it. The weather tool will now be available.

---

---

# 📧 MCP 2 — Gmail Server

Lets Claude read, send, and manage your Gmail.

## Part A — Google Cloud Setup

### Step 1 — Create a Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or select an existing one)
3. Enable the **Gmail API**: search for "Gmail API" in the search bar and click **Enable**

### Step 2 — Create OAuth Credentials

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. Choose **Desktop app** as the application type
4. Give it a name and click **Create**
5. Download the JSON file
6. Rename it to `gcp-oauth.keys.json`

---

## Part B — Authenticate

### Step 3 — Place your credentials file

```bash
mkdir -p ~/.gmail-mcp
mv gcp-oauth.keys.json ~/.gmail-mcp/
```

### Step 4 — Run authentication

```bash
npx @gongrzhe/server-gmail-autoauth-mcp auth
```

This will open your browser for Google sign-in. Once complete, credentials are saved to `~/.gmail-mcp/credentials.json` and can be reused from any directory.

---

## Part C — Connect to Claude Desktop

### Step 5 — Add to Claude Desktop config

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": [
        "@gongrzhe/server-gmail-autoauth-mcp"
      ]
    }
  }
}
```

### Step 6 — Restart Claude Desktop

Fully quit Claude (**⌘Q**) and reopen it. Claude can now interact with your Gmail.

---

---

# 🛠️ MCP 3 — Custom Server (FastMCP)

Build your own MCP tool from scratch using FastMCP.

### Step 1 — Navigate to your project folder

```bash
cd AI-Workshop/custom-mcp
```

### Step 2 — Create a virtual environment

```bash
uv venv
```

### Step 3 — Install dependencies

```bash
uv pip install httpx
uv pip install mcp
uv pip install fastmcp
```

### Step 4 — Create your server file `server.py`

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-tool")

@mcp.tool()
async def my_tool(input: str) -> str:
    """Describe what your tool does — Claude reads this description."""
    return f"You said: {input}"

if __name__ == "__main__":
    mcp.run()
```

The `@mcp.tool()` decorator is all Claude needs to discover and call your function. The docstring becomes the tool's description, so write it clearly!

### Step 5 — Test it

```bash
uv run server.py
```

### Step 6 — Add to Claude Desktop config

```json
{
  "mcpServers": {
    "my-tool": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/YOUR_USERNAME/AI-Workshop/custom-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Step 7 — Restart Claude Desktop

Fully quit Claude (**⌘Q**) and reopen it. Your custom tool is now live.

---

---

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed to spawn: No such file or directory` | `uv` path is wrong | Use the full path from `which uv` |
| `uv not found` | `uv` isn't installed | Run the install curl command and restart your terminal |
| `Request timed out` | First-run download is slow | Run `uv run weather.py` manually in terminal first |
| Config changes not taking effect | Claude wasn't fully quit | Use **⌘Q**, not just closing the window |
| `VIRTUAL_ENV does not match` warning | Outer venv conflict | Harmless — safely ignore it |

---

---

## 🆘 Installing Python & uv

### Install Python 3.13

**Mac:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click **Download Python 3.13.x** and run the `.pkg` installer
3. Open a new terminal and verify: `python3 --version`

**Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/) and run the installer
2. ⚠️ Check **"Add Python to PATH"** on the first screen
3. Open Command Prompt and verify: `python --version`

### Install `uv`

**Mac/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then close and reopen your terminal.

---

## 📖 Useful Links

- [MCP Official Docs](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [uv Documentation](https://docs.astral.sh/uv/)
- [MCP Debugging Guide](https://modelcontextprotocol.io/docs/tools/debugging)

---

## 💡 Ideas for Your Own MCP

- 📅 **Calendar tool** — Read/write Google Calendar events
- 🗄️ **Database tool** — Query a local SQLite database
- 🔎 **Search tool** — Wrap any REST API (news, stocks, sports)
- 📁 **File tool** — Read and summarize local documents
- 🏠 **Home automation** — Control smart home devices

---

*Made with ❤️ for the AI Hackathon*