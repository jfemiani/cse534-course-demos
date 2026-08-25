# 2d: HostedMCPTool talking to a real, external MCP server

Concept: `HostedMCPTool` lets an `Agent` use a real MCP server instead of a
demo one. This connects to DeepWiki (`https://mcp.deepwiki.com/mcp`), a
free, no-authentication MCP server that answers questions about public
GitHub repositories. OpenAI's side asks the server for its current tool
list, calls whichever tool the model picks, and the server runs it and
sends back the result — no code on our side executes for that call, same
as `WebSearchTool` in `02c_agent_loop_hosted_tools.py`, except this server
is not one OpenAI built.

## Compare with

- `02c_agent_loop_hosted_tools.py` — a hosted tool OpenAI built
  (`WebSearchTool`) mixed with a local function tool.
- `02e_agent_loop_mcp_raw_jsonrpc.py` — the same DeepWiki server, called
  with raw JSON-RPC instead of the Agents SDK, so you can see the actual
  requests and responses.

## Endpoint

OpenAI Agents SDK (`agents.Agent`, `agents.Runner`, `agents.HostedMCPTool`)
talking to `https://mcp.deepwiki.com/mcp`.

## Regeneration prompt

If the Agents SDK's `HostedMCPTool` config changes, ask an LLM assistant:
"Update this script to match the current OpenAI Agents SDK's
`HostedMCPTool`. Keep it pointed at the DeepWiki MCP server
(`https://mcp.deepwiki.com/mcp`) and keep the single question that asks
about a real public repo."
