from datetime import datetime
from google.adk.agents import Agent
from dotenv import load_dotenv
load_dotenv()

def get_current_time() -> str:
    """
    Returns the current datetime

    Args:
        None
    Returns:
        str: Current datetime in the format YYYY-MM-DD HH:MM:SS
    Example:
        >>> get_current_time()
        '2023-10-01 12:00:00'
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
    tools=[get_current_time],
)
