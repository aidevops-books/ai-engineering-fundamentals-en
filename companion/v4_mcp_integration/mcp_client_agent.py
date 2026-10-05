"""Chapter 10, Version 4 -- MCP Integration.

Launches mcp_server.py as a subprocess and talks to it over the stdio
transport (Chapter 10's "Transport" section) exactly the way a real MCP
host application would: connect, discover tools, call one.

This intentionally does NOT call an LLM -- it isolates the one thing that
actually changes between Version 3 and Version 4 (where the tool lives and
how its schema is discovered), so it can be verified end to end with no
API key required. Wiring the discovered tool schema into an actual agent
loop is exactly Chapter 10's agent_turn() from Version 3, unchanged --
only the `tools` list's origin changes.

Run:
    python mcp_client_agent.py
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_SCRIPT = Path(__file__).resolve().parent / "mcp_server.py"


async def main() -> None:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover tools -- the schema comes from the server, not this file.
            tools_result = await session.list_tools()
            tool_names = [t.name for t in tools_result.tools]
            print("Discovered tools from MCP server:", tool_names)

            # Call the tool exactly as an agent's tool-execution step would.
            result = await session.call_tool(
                "get_ticket_status", arguments={"ticket_id": "4471"}
            )
            print("Tool result:", result.content[0].text if result.content else result)


if __name__ == "__main__":
    asyncio.run(main())
