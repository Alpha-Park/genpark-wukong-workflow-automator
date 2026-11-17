---
description: One-Sentence Workflow Automator. Triggers complex, multi-app enterprise workflows from simple natural language commands.
license: MIT
metadata:
  last_deployed: "2026-04-25"
  version: "1.0.0"
  source: "https://wukong.dingtalk.com/"
---

# Wukong Workflow Automator

This skill allows for the creation and execution of "One-Sentence Super Actions." It maps complex, multi-step enterprise procedures to simple human language, acting as a conversational macro engine.

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.

## Instructions
1. **Procedural Mapping:** Interpret natural language commands and map them to known enterprise workflows (e.g., "Onboard user" -> [Account creation, Email welcome, Calendar invite]).
2. **Multi-App Execution:** Orchestrate the sequential or parallel execution of tasks across multiple enterprise platforms.
3. **Trigger Monitoring:** Listen for specific "magic phrases" or events to automatically fire off complex workflows.
4. **Conditional Logic:** Handle branch points in workflows (e.g., "If manager approval is required, send request and wait").

## Examples
- "Onboard the new marketing intern, Sarah. Set up her accounts, send her the welcome doc, and schedule a 1:1 with the CMO."
- "Close out Project Alpha. Archive the docs, notify the stakeholders in chat, and generate a final billing summary."
