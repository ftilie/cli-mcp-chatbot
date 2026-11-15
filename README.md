# MCP Chat — CLI Chatbot with the Model Context Protocol

A command-line chatbot built on Claude (Anthropic API) and the **Model Context Protocol (MCP)**. I built it as part of Anthropic's MCP course while working toward my certification.

The project has both sides of MCP:

- **An MCP server** ([mcp_server.py](mcp_server.py)): built with `FastMCP`. It exposes a small in-memory document store through **tools**, **resources** and **prompts**.
- **An MCP client** ([mcp_client.py](mcp_client.py)): it connects to the server over `stdio`, finds what the server offers, and gives it to Claude during a chat session.

## What I learned

- How MCP's three primitives differ:
  - **Tools** are *model-controlled*. Claude decides when to call them.
  - **Resources** are *app-controlled*. The application fetches data and adds it to the context.
  - **Prompts** are *user-controlled*. They are reusable prompt templates that the user runs as commands.
- How to build an MCP server with `FastMCP` decorators (`@mcp.tool`, `@mcp.resource`, `@mcp.prompt`).
- How to write an MCP client with `ClientSession` and `stdio_client`, and how to manage its lifecycle with `AsyncExitStack`.
- How to connect MCP tools to Claude's tool-use loop.

## Features

| Feature | MCP primitive | How to use it |
|---|---|---|
| Read a document | Tool: `read_doc_contents` | Ask Claude about a document |
| Edit a document | Tool: `edit_document` | Ask Claude to change a document |
| List document IDs | Resource: `docs://documents` | Used for `@` autocompletion |
| Fetch a document | Resource: `docs://documents/{doc_id}` | `@doc_id` in your message |
| Reformat as Markdown | Prompt: `format` | `/format <doc_id>` |
| Summarize a document | Prompt: `summarize_doc` | `/summarize_doc <doc_id>` |

## Project structure

```
.
├── main.py             # Entry point: starts the MCP client(s) and the CLI
├── mcp_server.py       # MCP server: document tools, resources and prompts
├── mcp_client.py       # MCP client wrapper around ClientSession
├── test_mcp_client.py  # Unit tests for the client
└── core/
    ├── claude.py       # Wrapper around the Anthropic API
    ├── chat.py         # Chat loop and tool-use handling
    ├── cli_chat.py     # @mentions (resources) and /commands (prompts)
    ├── cli.py          # prompt-toolkit CLI with autocompletion
    └── tools.py        # Collects and runs tools across MCP clients
```

## Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)
- [uv](https://github.com/astral-sh/uv) (recommended)

## Setup

### 1. Configure environment variables

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY="your-api-key"
CLAUDE_MODEL="claude-sonnet-5-5"
USE_UV=1   # set to 0 if you are not using uv
```

> `.env` is in `.gitignore`. Never commit your API key.

### 2. Install and run

**With uv (recommended)**

```bash
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv pip install -e .
uv run main.py
```

**Without uv**

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install "anthropic<1" python-dotenv prompt-toolkit "mcp[cli]>=1.8.0,<2"
python main.py
```

You can also connect more MCP servers by passing their scripts as arguments:

```bash
uv run main.py other_server.py
```

## Usage

**Chat:** type a message and press Enter.

**Add a document to your message with `@`:**

```
> Tell me about @deposition.md
```

**Run a server prompt with `/`:**

```
> /format report.pdf
> /summarize_doc plan.md
```

Commands and document IDs autocomplete when you press Tab.

## Testing

```bash
uv run python -m unittest test_mcp_client.py
```

You can also inspect the server on its own with the MCP Inspector:

```bash
uv run mcp dev mcp_server.py
```

## Adding documents

Documents live in the `docs` dictionary in [mcp_server.py](mcp_server.py). Add an entry there to make a new document available.

## Acknowledgements

Based on the starter project from Anthropic's MCP course.
