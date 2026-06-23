# 🔌 AI MCP Toolkit

> An MCP (Model Context Protocol) server exposing three AI capabilities — web research, code review, and concept explanation — as standardized tools any MCP-compatible client can call directly, including Claude Desktop.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![MCP](https://img.shields.io/badge/Protocol-MCP-5A2D82?style=flat-square)
![Groq](https://img.shields.io/badge/LLM-LLaMA%20%7C%20Groq-orange?style=flat-square)
![Tavily](https://img.shields.io/badge/Search-Tavily-blue?style=flat-square)

---

## 🎯 What It Does

Every AI client built before this protocol existed needed its own custom integration to call your code — a ChatGPT plugin works differently from a LangChain tool, which works differently from a CrewAI tool. MCP standardizes that. Write a tool once as an MCP server, and **any** MCP-compatible client — Claude Desktop, Claude Code, Cursor, or a custom agent — can discover and call it the same way, with no client-specific integration code.

This server exposes three tools, each reusing a capability already proven in an earlier project in this portfolio rather than rebuilding logic from scratch:

```
web_research        → Tavily search + Groq summarization   (from ai-research-agent)
review_code_diff    → structured code review feedback        (from ai-pr-reviewer)
explain_concept      → audience-tailored explanations          (new)
```

The point isn't the tools themselves — it's the exposure layer. Capabilities that previously only worked inside a FastAPI endpoint or a CrewAI agent now work inside **any** MCP client, with zero changes to the underlying logic.

---

## 📸 Screenshots

**MCP Inspector — tool schemas and live testing**
![MCP Inspector](screenshots/mcp-inspector.png)
Local dev tool showing all 3 tools auto-discovered from `@mcp.tool()` decorators, with their generated input/output schemas.

**Connected and running in Claude Desktop**
![Claude Desktop connection](screenshots/claude-desktop-running.png)
Settings → Developer → Local MCP servers, showing `ai-toolkit` with status `running`.

**A real tool call inside a Claude conversation**
![Tool call in action](screenshots/tool-call-in-chat.png)
Claude recognizing a request matches the `web_research` tool, invoking it, and returning a result grounded in live search — not its own training data.

---

## ✨ Features

- **Protocol-standard tool exposure** — built on the official MCP Python SDK (`FastMCP`), not a custom client integration
- **Auto-generated schemas** — tool input/output schemas are derived automatically from Python type hints and docstrings, no manual schema writing
- **Reused, not rebuilt** — each tool wraps logic already proven in a separate FastAPI project, demonstrating capability reuse across architectures
- **Client-agnostic** — works with Claude Desktop, Claude Code, MCP Inspector, or any future MCP-compatible client without code changes
- **Local-first development loop** — testable end-to-end via MCP Inspector before ever connecting a real client

---

## 🧠 How It Works

A tool in this server is just a Python function with a `@mcp.tool()` decorator. `FastMCP` inspects the function's type hints and docstring to generate the JSON schema a client needs to know what the tool does, what parameters it takes, and what it returns — none of that schema is written by hand.

```python
@mcp.tool()
def explain_concept(concept: str, audience: str = "a senior backend engineer new to AI") -> str:
    """Explain a technical or AI concept tailored to a specific audience's
    background level, using concrete analogies."""
    ...
```

When a client like Claude Desktop starts, it spawns this server as a subprocess and performs a handshake (`initialize` → `tools/list`) over stdio, using the MCP protocol — not HTTP. The client now knows all three tools exist and what they need, and can call any of them mid-conversation whenever a request matches.

One practical lesson from building this: a client with its own native capabilities (like Claude's built-in web search) may choose its own tool over your MCP tool for ambiguous requests, since both are valid ways to satisfy it. Naming the tool explicitly, or asking for something only your tool can do, removes that ambiguity — useful to know when demoing or debugging.

---

## 🗂️ Project Structure

```
ai-mcp-toolkit/
├── server.py        # All 3 tools, FastMCP server entry point
├── .env.example
└── .gitignore
```

One file. The simplicity is the point — this is the exposure layer, not where the heavy logic lives.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Groq API key](https://console.groq.com) — free
- [Tavily API key](https://tavily.com) — free

### Installation

```bash
git clone https://github.com/vyavahare-kishor/ai-mcp-toolkit
cd ai-mcp-toolkit

curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv add "mcp[cli]" groq tavily-python python-dotenv
```

### Configuration

```bash
cp .env.example .env
```
```bash
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Test locally — MCP Inspector

```bash
uv run mcp dev server.py
```

Opens a local web UI listing all 3 tools. Run each one directly to verify behavior before connecting a real client.

### Connect to Claude Desktop

Add to `claude_desktop_config.json` (Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ai-toolkit": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/ai-mcp-toolkit", "run", "server.py"]
    }
  }
}
```

Restart Claude Desktop. The tools icon should show `ai-toolkit` as connected, and all 3 tools become callable directly inside any conversation.

---

## 🗺️ Roadmap

- [ ] Add an MCP resource (not just tools) — expose read-only context like prior research results
- [ ] Add an MCP prompt template for a guided workflow (e.g. structured PR review request)
- [ ] Authentication for remote deployment (currently local-only, stdio transport)
- [ ] Wrap the ai-customer-support-bot RAG pipeline as a 4th tool

---

## 🔗 Related Projects

Part of an AI-native engineering portfolio. Full journey: [**ai-engineering-journey**](https://github.com/vyavahare-kishor/ai-engineering-journey)

| Project | Connection to this one |
|---------|--------------------------|
| [**ai-research-agent**](https://github.com/vyavahare-kishor/ai-research-agent) | `web_research` tool reuses this project's search + summarize pattern |
| [**ai-pr-reviewer**](https://github.com/vyavahare-kishor/pr-code-reviewer) | `review_code_diff` tool reuses this project's structured review approach |
| [**ai-analyst-crew**](https://github.com/vyavahare-kishor/ai-analyst-crew) | Same Groq backend, different exposure layer — agents vs. protocol-standard tools |

---

## 👨‍💻 Author

**Kishor Vyavahare**
Senior Software Engineer → AI Native Engineer

11+ years of backend engineering (Ruby on Rails, PostgreSQL, AWS).
Now building production AI systems — RAG pipelines, agents, multi-agent crews, and protocol-standard tool exposure via MCP.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/vyavahare-kishor)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/vyavahare-kishor)

---

## 📄 License

MIT License — use it, fork it, build on it.
