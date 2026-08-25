# pip install httpx

"""Demo 2e: talking to a real MCP server with raw JSON-RPC, no SDK involved.

See 02e_agent_loop_mcp_raw_jsonrpc.md for the full explanation.
"""

import json

import httpx

SERVER_URL = "https://mcp.deepwiki.com/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def call(client: httpx.Client, request: dict) -> dict:
    """Send one JSON-RPC request over HTTP and parse the response."""
    print("--- sent ---")
    print(json.dumps(request, indent=2))

    response = client.post(SERVER_URL, headers=HEADERS, json=request)
    # The server replies as one Server-Sent-Events message: a line starting
    # with "data:" that holds the actual JSON-RPC response.
    line = next(
        raw_line for raw_line in response.text.splitlines() if raw_line.startswith("data:")
    )
    reply = json.loads(line.removeprefix("data:").strip())

    print("--- received ---")
    print(json.dumps(reply, indent=2)[:1000])
    print()
    return reply


with httpx.Client(timeout=30) as client:
    # tools/list: ask the server what functions it currently offers.
    list_reply = call(
        client,
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
    )
    tool_names = [tool["name"] for tool in list_reply["result"]["tools"]]
    print(f"Tools this server offers: {tool_names}\n")

    # tools/call: invoke one of the tools we just discovered.
    call_reply = call(
        client,
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "read_wiki_structure",
                "arguments": {"repoName": "openai/openai-agents-python"},
            },
        },
    )
    result_text = call_reply["result"]["content"][0]["text"]
    print(f"Tool result:\n{result_text[:300]}...")
