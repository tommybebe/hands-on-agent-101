import os
from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER_NAME = os.getenv("JIRA_USER_NAME")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")

atlassian_mcp_agent = Agent(
    name="atlassian_mcp_agent",
    model='gemini-2.5-flash',
    description="manage issue from Jira and Confluence using MCP",
    instruction="You are a helpful Jira and Confluence manager. "
                "When the user asks for the issue or page, "
                "use tools to search, read, update, create issue and pages. "
                "for example, you can use 'jira_search' tool to search issue and 'confluence_search' tool to search pages. "
                "you can also use 'jira_get_issue' and 'confluence_get_page' tool to get issue and page details. "
                "you can even create/update/delete issue and pages. but you have to be careful and double check the result. "
                "if there's no specific request, then default to search in 'DATA' project and assigned currentUser and status in 'To Do', 'In Progress', 'In Review'"
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the issue list clearly.",
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='uvx',
                args=[
                    "mcp-atlassian",
                    f"--confluence-url={JIRA_URL}/wiki",
                    f"--confluence-username={JIRA_USER_NAME}",
                    f"--confluence-token={JIRA_TOKEN}",
                    f"--jira-url={JIRA_URL}",
                    f"--jira-username={JIRA_USER_NAME}",
                    f"--jira-token={JIRA_TOKEN}"
                ]
            ),
            # Optional: Filter which tools from the MCP server are exposed
            # tool_filter=['list_directory', 'read_file']
        )
    ],

)

root_agent = Agent(
    name="time_agent",
    model="gemini-2.0-flash",
    description=(
        "An agent that provides the current time when asked. "
        "It uses a simple tool to fetch the current datetime."
    ),
    instruction=(
        "if user asks for the current time, "
        "use the get_current_time tool to provide the current datetime."
        "If the user asks for something else, "
        "respond with your think about the question and provide a relevant answer."
    ),
    sub_agents=[atlassian_mcp_agent],
)
