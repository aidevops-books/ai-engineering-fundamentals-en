"""AI Knowledge Assistant -- Version 3: Agent + Tools (Chapter 10).

Requires OPENAI_API_KEY. The tool-calling schema and the get_ticket_status()
function themselves need no API key and are exercised directly under
__main__ so the non-LLM half of this file is still verified without one.

Run:
    OPENAI_API_KEY=sk-... python agent.py
"""

import json
import os

TICKET_DB = {"4471": "In Progress", "5502": "Resolved"}


def get_ticket_status(ticket_id: str) -> dict:
    # In a real system this would call an internal API or database.
    return {"ticket_id": ticket_id, "status": TICKET_DB.get(ticket_id, "Not Found")}


TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_ticket_status",
        "description": "Look up the current status of a support ticket by ID.",
        "parameters": {
            "type": "object",
            "properties": {"ticket_id": {"type": "string"}},
            "required": ["ticket_id"],
        },
    },
}]


def agent_turn(user_message: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    messages = [{"role": "user", "content": user_message}]

    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # illustrative model name -- see Chapter 1's note
        messages=messages, tools=TOOLS,
    )
    choice = resp.choices[0]

    if choice.finish_reason == "tool_calls":
        call = choice.message.tool_calls[0]
        args = json.loads(call.function.arguments)

        result = get_ticket_status(**args)

        messages.append(choice.message)
        messages.append({
            "role": "tool", "tool_call_id": call.id,
            "content": json.dumps(result),
        })
        final = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return final.choices[0].message.content

    return choice.message.content


if __name__ == "__main__":
    # Verify the tool logic itself, with no API key required.
    print("Direct tool call:", get_ticket_status("4471"))
    print("Tool schema:", json.dumps(TOOLS, indent=2))

    if os.environ.get("OPENAI_API_KEY"):
        print(agent_turn("What's the status of ticket 4471?"))
    else:
        print("\n(Set OPENAI_API_KEY to run the full agent loop.)")
