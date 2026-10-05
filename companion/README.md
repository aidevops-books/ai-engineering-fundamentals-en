# AI Knowledge Assistant — Companion Project

This is the standalone, runnable version of the book's running project, evolving version by version exactly as described in each chapter. Every version below has been executed end to end against the package versions noted in `requirements.txt` — see "What's actually verified" for exactly what that does and doesn't cover.

| Version | Chapter | What it adds | Needs an API key? |
|---|---|---|---|
| `v0_basic_model/` | 2 | A classical ML churn classifier | No |
| `v1_llm_application/` | 6 | A single system-prompted LLM call | Yes |
| `v2_rag_application/` | 9 | Retrieval + reranking, then a grounded LLM answer | Retrieval/rerank: no. Generation: yes |
| `v3_agent_tools/` | 10 | Tool calling — the model decides whether to look up a ticket | Tool logic: no. Full agent loop: yes |
| `v4_mcp_integration/` | 10 | The same tool exposed over a real MCP server instead of in-process code | No |
| `v5_production_system/` | 11 | A golden-dataset evaluation harness with LLM-as-a-judge, plus cost/latency logging | Yes |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # or .venv\Scripts\activate on Windows
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

Versions 1, 2 (with `--generate`), 3 (full agent loop), and 5 need a real OpenAI API key:

```bash
export OPENAI_API_KEY=sk-...   # or `set` on Windows cmd, $env: on PowerShell
```

## Running each version

```bash
python v0_basic_model/train_and_predict.py
python v1_llm_application/ask_assistant.py                 # needs OPENAI_API_KEY
python v2_rag_application/rag_assistant.py                  # retrieval + reranking only
python v2_rag_application/rag_assistant.py --generate       # + generation, needs OPENAI_API_KEY
python v3_agent_tools/agent.py                              # tool logic always; full loop needs OPENAI_API_KEY
python v4_mcp_integration/mcp_client_agent.py               # launches mcp_server.py itself
python v5_production_system/evaluate.py                     # needs OPENAI_API_KEY
```

## What's actually verified

Every script above has been run, not just read, against these package versions: `scikit-learn` 1.9.1, `sentence-transformers` 6.0.1, `openai` 3.13.0 (its `chat.completions.create`/`.parse`, `images.generate`, and tool-calling response shapes were checked directly against this version — see Chapter 1's note on model names for why the specific model string is a separate, faster-moving concern from the SDK shape), and `mcp` 2.x (`MCPServer`/`ClientSession` — note this is the v2 API; if you have `mcp<2` installed, `FastMCP` is the v1 equivalent of `MCPServer` and the import paths differ).

What this verification does **not** cover: the actual *content* of a live LLM response (no API key was used to generate this project, so `v1`, `v2 --generate`, `v3`'s full agent loop, and `v5` were verified for correct wiring and graceful failure without a key, not for response quality) — and that a specific model name (`gpt-4o-mini` throughout) is still available and current on the day you run this, which is exactly the kind of detail Chapter 1's note asks you to verify yourself before relying on it.

## Project layout

```
companion/
├── shared/                churn_data.py, knowledge_base.py -- reused across versions
├── v0_basic_model/
├── v1_llm_application/
├── v2_rag_application/
├── v3_agent_tools/
├── v4_mcp_integration/    a real MCP server + client, not just a code sketch
└── v5_production_system/
```
