"""Sample Parallelization pattern using LangChain LCEL."""

import asyncio
import logging
import warnings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI

# Ignore all warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# A "creative" model for more interesting outputs!
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

summarize_chain: Runnable = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                Summarize the following topic concisely.
                """,
            ),
            ("user", "{topic}"),
        ]
    )
    | llm
    | StrOutputParser()
)

question_chain: Runnable = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                Generate three interesting questions about the following topic.
                """,
            ),
            ("user", "{topic}"),
        ]
    )
    | llm
    | StrOutputParser()
)

key_terms_chain: Runnable = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                Identify 5-10 key terms from the following topic, separated by commas.
                """,
            ),
            ("user", "{topic}"),
        ]
    )
    | llm
    | StrOutputParser()
)


# Build the parallel + synthesis chain
map_chain: Runnable = RunnableParallel(
    {
        "summary": summarize_chain,
        "questions": question_chain,
        "key_terms": key_terms_chain,
        "topic": RunnablePassthrough(),  # Pass the original topic through
    }
)

synthesis_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Based on the following information:
            - Summary: {summary}
            - Questions about the topic: {questions}
            - Key terms: {key_terms}
            Synthesize a comprehensive answer.
            """,
        ),
        ("user", "Original topic: {topic}"),
    ]
)

full_parallel_chain = map_chain | synthesis_prompt | llm | StrOutputParser()


async def run_parallel_chain(topic: str) -> str:
    """Runs the full parallelization chain asynchronously.
    Args:
        topic (str): The topic to process.
    Returns:
        str: The synthesized answer based on the summary, questions, and key terms.
    """
    try:
        return await full_parallel_chain.ainvoke(topic)
    except Exception as e:
        error_message = f"An error occurred while processing the topic: {e}"
        logging.error(error_message)
        return error_message


if __name__ == "__main__":
    topic = "The impact of climate change on global agriculture."
    synthesized_answer = asyncio.run(run_parallel_chain(topic))
    logging.info(synthesized_answer)
