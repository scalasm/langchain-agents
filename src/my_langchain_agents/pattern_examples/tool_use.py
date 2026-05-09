"""Sample Parallelization pattern using LangChain LCEL."""

import asyncio
import logging
import warnings

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_protocol import Any

# Ignore all warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# A "creative" model for more interesting outputs!
llm = ChatOpenAI(model="gpt-4.1", temperature=0.7)


@tool
def search_information(query: str) -> str:
    """Simulates a search tool by returning a string based on the query.
    In a real implementation, this could be an API call to a search engine or database.
    Args:
        query (str): The search query.
    Returns:
        str: Simulated search results.
    """
    simulated_results = {
        "What is the capital of France?": "The capital of France is Paris.",
        "Weather in London": "The current weather in London is cloudy with a chance of rain.",
        "population in Italy": "The population of Italy is approximately 60 million people.",
        "tallest mountain": "The tallest mountain in the world is Mount Everest, which stands at 8,848 meters (29,029 feet) above sea level.",
        "default": f"Sorry, I don't have information about: '{query}'",
    }
    return simulated_results.get(query, simulated_results.get(query.lower(), simulated_results["default"]))


tools = [search_information]

agent_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

helpful_agent = create_agent(name="helpful-agent", model=llm, tools=tools, system_prompt="You are a helpful assistant.")


async def get_content_from_response(response: dict[str, Any]) -> str:
    """Extracts the content from the agent's response messages.

    Args:
        response (dict[str, Any]): The agent's response containing messages.

    Returns:
        str: The content of the last AIMessage in the response, or an empty string if none found.
    """
    messages = response.get("messages", [])
    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            return str(msg.content)
    return ""


async def run_agent_with_tool(user_input: str) -> None:
    logging.info(f"User input: {user_input}")
    response: dict[str, Any] = await helpful_agent.ainvoke({"messages": [HumanMessage(content=user_input)]})
    content = await get_content_from_response(response)
    logging.info(f"Extracted content: {content}")


async def main() -> None:
    await run_agent_with_tool("What is the capital of France?")
    await run_agent_with_tool("Weather in London")
    await run_agent_with_tool("Something I don't know about")


if __name__ == "__main__":
    asyncio.run(main())
