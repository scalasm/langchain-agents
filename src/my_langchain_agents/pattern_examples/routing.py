"""Sample Routing patterns."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1", temperature=0)


def booking_request_handler(request: str) -> str:
    """Simulates the Booking Agent handling a request."""
    print("Booking Agent received request:", request)
    return f"Booking Agent: Your flight has been booked '{request}'."


def info_request_handler(request: str) -> str:
    """Simulates the Information Agent handling a request."""
    print("Information Agent received request:", request)
    return f"Information Agent: Here is the information you requested about '{request}'."


def unclear_request_handler(request: str) -> str:
    """Simulates handling an unclear request."""
    print(f"Coordinator could not delegate the request: {request}")
    return "Coordinator: I'm sorry, I couldn't understand your request. Could you please clarify?"


# Define coordinator router chain
coordinator_router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Analyze the user's request and determine which specialist handler should process it.
                - if the request is related to booking flights or hotels, output 'booker'.
                - For weather or sea conditions, output 'info'
                - if the request is unclear or doesn't fit the above categories, output 'unclear'
            ONLY output one word: 'booker', 'info', or 'unclear'.
            """,
        ),
        ("user", "{request}"),
    ]
)

# Create the coordinator_router_chain, which takes the user's request and determines
# which handler should process it.
coordinator_router_chain = coordinator_router_prompt | llm | StrOutputParser()

# Create a delegation branch, which takes which will route the 'request' to the appropriate handler
branches = {
    "booker": RunnablePassthrough.assign(output=lambda x: booking_request_handler(x["request"]["request"])),
    "info": RunnablePassthrough.assign(output=lambda x: info_request_handler(x["request"]["request"])),
    "unclear": RunnablePassthrough.assign(output=lambda x: unclear_request_handler(x["request"]["request"])),
}

delegation_branch = RunnableBranch(
    (lambda x: x["decision"].strip() == "booker", branches["booker"]),
    (lambda x: x["decision"].strip() == "info", branches["info"]),
    branches["unclear"],  # Default branch for 'unclear' or any unrecognized decision
)

# The coordinator_agent first determines which handler should process the request using
# the coordinator_router_chain, then delegates the request to the appropriate handler
# using the delegation_branch, and finally returns the output from the handler.
coordinator_agent = (
    {"decision": coordinator_router_chain, "request": RunnablePassthrough(input_key="request")}
    | delegation_branch
    | (lambda x: x["output"])
)


def main() -> None:
    """Main function to simulate user requests to the coordinator agent."""
    request = "Book me a flight to Dublin next week."
    response = coordinator_agent.invoke({"request": request})
    print(response)

    request = "How is the weather in Paris?"
    response = coordinator_agent.invoke({"request": request})
    print(response)

    request = "How much is 1 + 1 ?."
    response = coordinator_agent.invoke({"request": request})
    print(response)


if __name__ == "__main__":
    main()
