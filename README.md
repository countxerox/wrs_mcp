# Windchill MCP Connector

Minimal, production-ready [Model Context Protocol](https://github.com/modelcontextprotocol) server exposing
read-only access to PTC Windchill.

## Features
- ✅ Stdio transport MCP server using the official Python SDK.
- ✅ Tools: `health_check`, `list_parts`, `get_part`.
- ✅ Defensive HTTP client with timeouts, TLS verification, and auth token.
- ✅ Linting (ruff), testing (pytest), and GitHub Actions CI.

## Architecture
```
+------------+      stdio      +--------------------+
| ChatGPT    | <-------------> | windchill-mcp      |
| (Developer)|                 |  WindchillClient   |
+------------+                 +---------+----------+
                                        |
                                        | HTTPS REST/OData
                                        v
                                    PTC Windchill
```

## Setup
1. **Clone and install**
   ```bash
   git clone https://github.com/ORG/REPO_NAME.git
   cd REPO_NAME
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Configure environment** – copy `.env.example` → `.env` and edit values:
   - `WINDCHILL_BASE_URL`
   - `WINDCHILL_API_TOKEN`
   - `VERIFY_TLS` (`true`/`false`)
   - `HTTP_TIMEOUT_SECONDS`

## Running
```bash
python server.py
```
The server prints a single line and waits on stdio for MCP requests.

## ChatGPT Custom Connector
1. Enable **Developer Mode** in ChatGPT → *Settings → Connectors*.
2. Add a **Custom Connector** pointing at this repo's `mcp.json`.
3. Tools `health_check`, `list_parts`, `get_part` appear for use.

### Example Calls
```jsonc
// health_check
{"tool": "health_check", "arguments": {}}
// → {"ok": "true", "base_url": "https://plm.example.com/..."}

// list_parts
{"tool": "list_parts", "arguments": {"container": "Demo", "limit": 2}}
// → [{"partNumber": "123", "name": "Bolt", ...}, ...]

// get_part
{"tool": "get_part", "arguments": {"partNumber": "123"}}
// → {"partNumber": "123", "name": "Bolt", ...}
```

## Security Notes
- Read-only tools; no mutations.
- Use a low-privilege service account token.
- TLS verification enabled by default.
- Consider rate limiting and audit logging when extending.

## Troubleshooting
| Symptom | Fix |
|---------|-----|
| `401 Unauthorized` | Ensure `WINDCHILL_API_TOKEN` is valid. |
| SSL certificate errors | Set `VERIFY_TLS=false` only for testing. |
| Hanging requests | Check network connectivity or reduce `HTTP_TIMEOUT_SECONDS`. |

## Roadmap
- Input validation and richer models.
- More endpoints (search, BOM, change notices).
- Optional caching and rate limiting.

## Next steps
Ideas for expansion:
- `search_documents(query)`
- `get_bom(partNumber, depth)`
- `list_change_notices(container, state, limit)`
