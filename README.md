# wrs_mcp
wrs_mcp
Windchill MCP Connector
This repository contains a custom Model Context Protocol (MCP) server for PTC Windchill.
It exposes a read-only API to Windchill objects (e.g. WTParts) so that AI assistants like ChatGPT (with Developer Mode enabled) can query product data in a controlled and secure way.
✨ Features
Implements an MCP server using the official Python SDK.
Exposes Windchill data as simple, AI-friendly tools:
health_check → verify connection
list_parts → list recent WTParts in a container
get_part → fetch details for a single WTPart
Uses Windchill REST/OData endpoints (swap in your own paths).
Ships with a manifest (mcp.json) so it can be registered as a ChatGPT connector.
Designed for read-only access by default.
📂 Project Structure
windchill-mcp/
├─ server.py          # MCP server implementation (Python)
├─ mcp.json           # Connector manifest
├─ requirements.txt   # Python dependencies
└─ README.md          # Documentation
🚀 Getting Started
1. Clone & Setup
git clone https://github.com/your-org/windchill-mcp.git
cd windchill-mcp

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
2. Configure Environment
Set the following environment variables (e.g. in .env or shell):
export WINDCHILL_BASE_URL="https://plm.example.com/Windchill/servlet/odata/v3"
export WINDCHILL_API_TOKEN="your_service_token_here"
export VERIFY_TLS=true
3. Run the MCP Server
python server.py
This will launch the MCP server on stdio transport, ready for ChatGPT or another MCP client.
🔗 Using with ChatGPT
In ChatGPT, go to Settings → Connectors → Advanced.
Enable Developer Mode.
Add a Custom Connector and point it to this repo’s mcp.json.
The tools (health_check, list_parts, get_part) will appear as callable actions in ChatGPT.
🛡️ Security & Safety
Read-only by default – no mutations (create, revise, delete) are exposed.
Requires a service account token or API key with limited scope.
Always validate and sanitize input when extending with new tools.
If you add write tools (e.g. create Change Notices), ensure you implement explicit confirmation and audit logging.
🧩 Extending
Add new tools to server.py to expose other Windchill endpoints, for example:
search_documents(query, container, limit)
get_bom(partNumber, depth)
list_change_notices(container, state, limit)
⚠️ Disclaimer
This connector is provided as a starting point.
You are responsible for ensuring compliance with your company’s IT security policies, export controls, and data governance rules before deploying in production.
📜 License
Proprietary – for internal use only (adapt as needed).
