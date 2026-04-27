"""Routing with Google ADK (Agent Development Kit)."""

import logging
import traceback
import uuid
import warnings

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # For multi-model support
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool
from google.genai import types

# Ignore all warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# LitLLM is needed for anything but Google models
LLM_MODEL = LiteLlm("openai/gpt-4.1")


def booking_request_handler(request: str) -> str:
    """Handles booking requests for flights or hotels.

    Args:
        request (str): The user's booking request.

    Returns:
        str: A response indicating the booking status.
    """
    logging.info("Booking Agent received request: %s", request)
    return f"Booking Agent: Your booking request for '{request}' has been processed successfully."


def info_request_handler(request: str) -> str:
    """Handles general information requests.

    Args:
        request (str): The user's information request.

    Returns:
        str: A response containing the requested information.
    """
    logging.info("Information Agent received request: %s", request)
    return f"Information Agent: Here is the information you requested about '{request}'."


def unclear_request_handler(request: str) -> str:
    """Handles unclear requests that do not fit the booking or information categories.

    Args:
        request (str): The user's unclear request.

    Returns:
        str: A response asking the user to clarify their request.
    """
    logging.info("Coordinator could not delegate the request: %s", request)
    return "Coordinator: I'm sorry, I couldn't understand your request. Could you please clarify?"


booking_tool = FunctionTool(booking_request_handler)
info_tool = FunctionTool(info_request_handler)

# Define custom agents for booking and information handling
booking_agent = Agent(
    name="booking", model=LLM_MODEL, tools=[booking_tool], description="Handles booking requests for flights or hotels."
)
info_agent = Agent(
    name="info",
    model=LLM_MODEL,
    tools=[info_tool],
    description="Handles general information requests.",
)

coordinator_agent = Agent(
    name="coordinator",
    model=LLM_MODEL,
    instruction="""
        You are the main coordinator. Your only task is to analyze incoming user
        requests and delegate them to the appropriate specialist agent.
        Do not try to answer the user directly
        - For any request related to booking flights or hotels, delegate tot 'booking' agent.
        - For all other general information requests, delegate to 'info' agent.
    """,
    description="A coordinator agent that routes user requests to the appropriate specialist agent based on the content of the request.",
    # The presence of sub-agents enables LLM-driven delegation (auto flow) by default.
    sub_agents=[booking_agent, info_agent],
)


# Main execution logic
async def run_coordinator_agent(runner: InMemoryRunner, request: str) -> str:
    """Runs the coordinator agent with a given user request and returns the response.

    Args:
        runner (InMemoryRunner): The ADK runner to execute the agent.
        request (str): The user's request to be processed by the coordinator agent.
    Returns:
        str: The final response from the coordinator agent after delegation.
    """
    final_result = ""

    try:
        user_id = "user_123"  # Simulated user ID for tracking
        session_id = str(uuid.uuid4())  # Simulated session ID for tracking
        await runner.session_service.create_session(app_name=runner.app_name, session_id=session_id, user_id=user_id)

        for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(role="user", parts=[types.Part(text=request)]),
        ):
            if event.is_final_response() and event.content:
                # Try to get text directly from event.content to avoid iterating parts
                if hasattr(event.content, "text") and event.content.text:
                    final_result = event.content.text
                elif event.content.parts:
                    final_result = " ".join(part.text for part in event.content.parts if hasattr(part, "text") and part.text)
                logging.info("Final response from Coordinator Agent: %s", final_result)
                break  # Exit loop after processing the final response
        logging.info("Coordinator final response for %s: %s", user_id, final_result)
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred while processing the request: {e!s}"
        logging.error(error_message)
        return error_message


async def main() -> None:
    logging.info("Starting Coordinator Agent with Google ADK...")
    runner = InMemoryRunner(coordinator_agent)
    result = await run_coordinator_agent(runner, "Book me a flight to Dublin next week.")
    logging.info("Final result: %s", result)

    result = await run_coordinator_agent(runner, "What's the weather like in New York?")
    logging.info("Final result: %s", result)

    result = await run_coordinator_agent(runner, "I want to know about the stock market.")
    logging.info("Final result: %s", result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
