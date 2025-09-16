"""
Jira MCP client factory module
Handles dynamic creation of Jira/Atlassian MCP clients based on HTTP headers
"""

from fastmcp.server.proxy import ProxyClient
from fastmcp.client.transports import StdioTransport
from fastmcp.utilities.logging import get_logger

logger = get_logger(__name__)

def create_dynamic_jira_client_factory():
    """
    Creates a client factory that extracts Jira/Atlassian environment variables from HTTP headers
    and creates a new ProxyClient instance with those variables for each request.
    JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN are required.
    CONFLUENCE_URL, CONFLUENCE_USERNAME, and CONFLUENCE_API_TOKEN are optional.
    """
    def client_factory():
        try:
            # Get HTTP headers from the current request
            from fastmcp.server.dependencies import get_http_headers
            headers = get_http_headers()
            
            # Extract Jira/Atlassian environment variables from headers
            jira_url = headers.get('x-jira-url')
            jira_username = headers.get('x-jira-username')
            jira_api_token = headers.get('x-jira-api-token')
            confluence_url = headers.get('x-confluence-url')
            confluence_username = headers.get('x-confluence-username')
            confluence_api_token = headers.get('x-confluence-api-token')
            
            if jira_url and jira_username and jira_api_token:
                logger.info(f"Creating Jira client for {jira_url}")
                
                # Build environment variables dict with required values
                env_vars = {
                    "JIRA_URL": jira_url,
                    "JIRA_USERNAME": jira_username,
                    "JIRA_API_TOKEN": jira_api_token
                }
                
                # Add optional Confluence variables if provided
                if confluence_url:
                    env_vars["CONFLUENCE_URL"] = confluence_url
                if confluence_username:
                    env_vars["CONFLUENCE_USERNAME"] = confluence_username
                if confluence_api_token:
                    env_vars["CONFLUENCE_API_TOKEN"] = confluence_api_token
                
                # Create StdioTransport with Docker command and extracted environment variables
                transport = StdioTransport(
                    command="docker",
                    args=[
                        "run",
                        "-i",
                        "--rm",
                        "-e", "CONFLUENCE_URL",
                        "-e", "CONFLUENCE_USERNAME", 
                        "-e", "CONFLUENCE_API_TOKEN",
                        "-e", "JIRA_URL",
                        "-e", "JIRA_USERNAME",
                        "-e", "JIRA_API_TOKEN",
                        "ghcr.io/sooperset/mcp-atlassian:latest"
                    ],
                    env=env_vars
                )
                
                # Create ProxyClient with the transport
                return ProxyClient(transport)
            else:
                missing_params = []
                if not jira_url:
                    missing_params.append("x-jira-url")
                if not jira_username:
                    missing_params.append("x-jira-username")
                if not jira_api_token:
                    missing_params.append("x-jira-api-token")
                logger.warning(f"Missing required Jira headers: {', '.join(missing_params)}")
                return None
                
        except Exception as e:
            logger.error(f"Error in Jira client factory: {e}")
            return None
    
    return client_factory
