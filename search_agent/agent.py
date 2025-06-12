from google.adk.agents import LlmAgent
from google.adk.tools import SearchTool

agent = LlmAgent(
    name="search_agent",
    model="models/gemini-1.5-flash", # Or your preferred Gemini model
    description="A specialized agent that uses Google Search to find information.",
    instructions="You are a web search specialist. Your only job is to use the provided search tool to find factual, up-to-date information to answer a user's query. Provide the raw search results.",
    tools=SearchTool
)