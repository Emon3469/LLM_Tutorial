## Run the server

From this directory, use FastMCP's `run` subcommand:

```powershell
.\.venv\Scripts\fastmcp.exe run main.py
```

Do not run `fastmcp main.py`. `main.py` is not a FastMCP command; it is the
server specification passed to `run`.

The server uses stdio by default, which is the transport expected by most MCP
clients. To inspect the registered tools without starting the server:

```powershell
.\.venv\Scripts\fastmcp.exe inspect main.py
```

## Open the Inspector UI

To run the server with the MCP Inspector browser UI:

```powershell
uv run fastmcp dev inspector main.py
```

FastMCP prints a tokenized URL similar to this one:

```text
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<token>
```

Open the exact URL printed in the terminal. The Inspector UI uses port `6274`
and its proxy uses port `6277` by default.

On Windows, launching through `uv run` is recommended because the Inspector
starts the STDIO command from a child process and `uv` makes the project's
virtual environment available to it.