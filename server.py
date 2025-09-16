import contextlib
from fastapi import FastAPI
from fastmcp.server.proxy import FastMCPProxy
from fastmcp.utilities.logging import get_logger
from clients.slack_factory import create_dynamic_slack_client_factory
from clients.jira_factory import create_dynamic_jira_client_factory
import os

logger = get_logger(__name__)

slack_mcp = FastMCPProxy(
    client_factory=create_dynamic_slack_client_factory(),
    name="Slack MCP Server"
)

jira_mcp = FastMCPProxy(
    client_factory=create_dynamic_jira_client_factory(),
    name="Jira MCP Server"
)

slack_app = slack_mcp.http_app()
jira_app = jira_mcp.http_app()

# Create a combined lifespan to manage both MCP servers
@contextlib.asynccontextmanager
async def combined_lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(slack_app.lifespan(app))
        await stack.enter_async_context(jira_app.lifespan(app))
        
        logger.info("MCP servers started successfully")
        yield
        logger.info("MCP servers shutting down")

app = FastAPI(
    title="Zunou MCP Servers",
    description="Zunou MCP Servers",
    version="1.0.0",
    lifespan=combined_lifespan
)

app.mount("/slack", slack_app)
app.mount("/jira", jira_app)

PORT = os.environ.get("PORT", 10000)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
