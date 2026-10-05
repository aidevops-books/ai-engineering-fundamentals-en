"""Chapter 10, Version 4 -- the ticket-lookup tool exposed over MCP instead
of being hand-registered as a local Python function (Version 3).

Run standalone to sanity-check the server on its own:
    python mcp_server.py
(it will just idle waiting for a client on stdio -- Ctrl+C to stop)

Normally this file is launched automatically, as a subprocess, by
mcp_client_agent.py -- you do not run it directly in that flow.
"""

from mcp.server.mcpserver import MCPServer

server = MCPServer(name="tickets-server")

# The same fake data used in the book's Chapter 10 in-process example --
# in a real system this would call the ticket system's own database or API.
_FAKE_TICKETS = {"4471": "In Progress", "5502": "Resolved"}


@server.tool()
def get_ticket_status(ticket_id: str) -> dict:
    """Look up the current status of a support ticket by ID."""
    return {"ticket_id": ticket_id, "status": _FAKE_TICKETS.get(ticket_id, "Not Found")}


if __name__ == "__main__":
    server.run(transport="stdio")
