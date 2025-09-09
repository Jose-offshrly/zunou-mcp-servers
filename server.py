from fastmcp import FastMCP
from fastmcp.server.proxy import FastMCPProxy, ProxyClient
from fastmcp.server.dependencies import get_http_headers
from fastmcp.client.transports import StdioTransport
from fastmcp.utilities.logging import get_logger
import os

logger = get_logger(__name__)

def create_dynamic_slack_client_factory():
    """
    Creates a client factory that extracts Slack environment variables from HTTP headers
    and creates a new ProxyClient instance with those variables for each request.
    SLACK_BOT_TOKEN and SLACK_TEAM_ID are required, SLACK_CHANNEL_IDS is optional.
    """
    def client_factory():
        try:
            # Get HTTP headers from the current request
            headers = get_http_headers()
            
            # Extract Slack environment variables from headers
            slack_token = headers.get('x-slack-bot-token')
            slack_team_id = headers.get('x-slack-team-id')
            slack_channel_ids = headers.get('x-slack-channel-ids')
            
            if slack_token and slack_team_id:
                logger.info(f"Creating Slack client for team {slack_team_id}")
                
                # Build environment variables dict with required values
                env_vars = {
                    "SLACK_BOT_TOKEN": slack_token,
                    "SLACK_TEAM_ID": slack_team_id
                }
                
                # Add optional channel IDs if provided
                if slack_channel_ids:
                    env_vars["SLACK_CHANNEL_IDS"] = slack_channel_ids
                
                # Create StdioTransport with extracted environment variables
                transport = StdioTransport(
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-slack"],
                    env=env_vars
                )
                
                # Create ProxyClient with the transport
                return ProxyClient(transport)
            else:
                missing_params = []
                if not slack_token:
                    missing_params.append("x-slack-bot-token")
                if not slack_team_id:
                    missing_params.append("x-slack-team-id")
                logger.warning(f"Missing required Slack headers: {', '.join(missing_params)}")
                return None
                
        except Exception as e:
            logger.error(f"Error in client factory: {e}")
            return None
    
    return client_factory

# Create proxy with custom client factory for dynamic environment variables
proxy = FastMCPProxy(
    client_factory=create_dynamic_slack_client_factory(),
    name="Zunou MCP Servers"
)

# Run
port = os.environ.get("PORT", 8080)
if __name__ == "__main__":
    proxy.run(
        transport="http",
        host="0.0.0.0",  # Bind to all interfaces
        port=port         # Choose your preferred port
    )