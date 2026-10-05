"""AI Knowledge Assistant -- Version 1: LLM Application (Chapter 6).

Requires OPENAI_API_KEY to be set in the environment. Everything except the
actual network call has been verified against the currently installed
`openai` SDK's response shape (see companion/README.md).

Run:
    export OPENAI_API_KEY=sk-...   # or `set` on Windows cmd, $env: on PowerShell
    python ask_assistant.py
"""

import os

from openai import OpenAI


def ask_assistant(question: str, temperature: float = 0.3) -> str:
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # illustrative model name -- see Chapter 1's note
        messages=[
            {"role": "system", "content":
                "You are a concise, accurate assistant for internal engineering questions. "
                "If you are not confident in an answer, say so explicitly."},
            {"role": "user", "content": question},
        ],
        temperature=temperature,
    )
    usage = resp.usage
    print(f"tokens -- prompt: {usage.prompt_tokens}, "
          f"completion: {usage.completion_tokens}, "
          f"total: {usage.total_tokens}")
    return resp.choices[0].message.content


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit(
            "Set OPENAI_API_KEY before running this script -- "
            "Version 1 onward calls a real LLM API."
        )
    answer = ask_assistant("What is the difference between fine-tuning and RAG?")
    print(answer)
