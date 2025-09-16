# Zunou MCP Servers

A unified FastAPI-based MCP server that manages multiple MCP services (Slack and Jira) with dynamic header-based authentication.

## Servers

- **Slack MCP**: `/jira/mcp` - Slack tools and functionality
- **Jira MCP**: `/jira/mcp` - Jira/Atlassian tools and functionality

## Installation & Running

```bash
# Install dependencies
uv sync

# Run the server
uv run server.py
```

## Usage

### Slack MCP Server

**Endpoint**: `POST http://localhost:10000/mcp`

**Required Headers**:
- `x-slack-bot-token`: Your Slack bot token
- `Accept`: `application/json, text/event-stream`

**Optional Headers**:
- `x-slack-team-id`: Your Slack team ID
- `x-slack-channel-ids`: Comma-separated list of channel IDs


### Jira MCP Server

**Endpoint**: `POST http://localhost:10000/mcp`

**Required Headers**:
- `x-jira-url`: Your Jira instance URL
- `x-jira-username`: Your Jira username/email
- `x-jira-api-token`: Your Jira API token
- `Accept`: `application/json, text/event-stream`

**Optional Headers**:
- `x-confluence-url`: Confluence URL
- `x-confluence-username`: Confluence username
- `x-confluence-api-token`: Confluence API token