## Run the server

This project uses FastMCP with Python 3.13 and the local virtual environment.

### Run with the MCP Inspector

From this directory, start Inspector through `uv` so its child process can
resolve the virtual environment's `fastmcp` executable:

```powershell
uv run fastmcp dev inspector main.py
```

Open the tokenized URL printed by the command, for example:

```text
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<current-token>
```

The token is regenerated each time Inspector starts. Do not reuse an old URL.

### Run as an HTTP server

```powershell
.\.venv\Scripts\python.exe main.py
```

The Streamable HTTP endpoint is:

```text
http://127.0.0.1:8000/mcp
```

When the server is used with STDIO, startup diagnostics must remain on
stderr; stdout is reserved for MCP JSON-RPC messages.