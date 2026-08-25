# 2e: Talking to an MCP server with raw JSON-RPC

Concept: this demo skips the Agents SDK entirely and talks to a real,
public MCP server (DeepWiki, `https://mcp.deepwiki.com/mcp`) by sending
plain JSON-RPC 2.0 requests over HTTP with `httpx`. It calls `tools/list`
to get the server's current tool names, descriptions, and JSON Schemas,
then calls `tools/call` to invoke `read_wiki_structure` on a real GitHub
repo. Every request and response is printed in full, so you can see the
exact JSON-RPC envelope `HostedMCPTool` (in `02d_agent_loop_mcp.py`) is
sending on your behalf.

DeepWiki's server accepts both calls without an `initialize` handshake or
session ID, and replies using the Server-Sent-Events framing the
Streamable HTTP transport uses (`data: {...}`), even though we only sent
a plain POST. This demo peels that one layer of formatting off so you see
the underlying JSON-RPC message.

## Compare with

- `02d_agent_loop_mcp.py` — the same DeepWiki server, called through the
  Agents SDK's `HostedMCPTool` instead of raw JSON-RPC.

## Endpoint

`https://mcp.deepwiki.com/mcp` — a free, no-authentication MCP server
(Streamable HTTP transport).

## Regeneration prompt

If DeepWiki's tools or schema change, ask an LLM assistant: "Update this
script to match the current DeepWiki MCP server. Keep the raw JSON-RPC
`tools/list` then `tools/call` structure and print each request and
response in full; do not switch to an MCP SDK client."
