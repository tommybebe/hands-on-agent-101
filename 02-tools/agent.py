from google.adk.agents import Agent
from dotenv import load_dotenv
load_dotenv()

root_agent = Agent(
    name="hello_world_agnet",
    model="gemini-2.0-flash",
    description=(
        "Just a simple agent that says hello to the user. "
        "It does not use any tools or advanced features, just a basic interaction."
    ),
    instruction=(
        "whatever user says, just say hello back."
    )
)