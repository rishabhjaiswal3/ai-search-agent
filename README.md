# FirstAgent

Small learning repo for building an **LLM agent** with **LangChain** that can call **tools** (example: Tavily web search).

## What’s inside

- **Agent runtime**: `langchain>=1.3` (`create_agent`)
- **LLM**: OpenAI via `langchain-openai`
- **Tooling**: Tavily via `langchain-tavily`
- **Env loading**: `python-dotenv`
- **Package manager**: `uv` (`pyproject.toml` + `uv.lock`)

## Prerequisites

- Python **3.11+** (this repo uses `.python-version`)
- [`uv`](https://github.com/astral-sh/uv) installed

## Install

```bash
uv sync
```

## Configure environment variables

Create a local `.env` file (it is ignored by git on purpose).

Minimum:

```bash
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

Optional (LangSmith tracing):

```bash
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=lsv2_...your_key...
LANGSMITH_PROJECT=FirstAgent
```

## Run

```bash
uv run main.py
```

## How tool outputs work (important)

- A **tool** function (decorated with `@tool`) returns **data** (string/dict/etc).
- The **agent** calls the tool (if the model decides to), and the tool result is added to the conversation as a **ToolMessage**.
- Then the **model** generates the final **AIMessage**. That final text is what you usually print.

So if you expect `"This is a test search result"`:

- first confirm the tool returns it (direct tool call)
- then inspect the agent’s `result["messages"]` to see the ToolMessage and the final AIMessage

## Common issues

### Proxy / `403 Forbidden`

If you see errors like `ProxyError: 403 Forbidden`, your network/proxy is blocking outbound API calls (OpenAI/Tavily/LangSmith).

Fix options:

- Remove/adjust proxy env vars (`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`) for your terminal session
- Use a network where these APIs are accessible
- Switch to a local model (e.g. Ollama) if you want to develop offline

## Repo hygiene

- Do **not** commit `.env` (contains secrets)
- Do **commit** `uv.lock` (reproducible installs)
