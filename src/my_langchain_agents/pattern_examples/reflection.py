"""Demonstrate reflection pattern using LangChain.

The implementation uses a simple iteration to refine the LLM answer until it meets the
quality requirements.
"""

import logging
import warnings

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Ignore all warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# A more deterministing model for more consistent outputs!
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)


def run_reflection_loop() -> None:
    task_prompt = """
    Your task is to create a Python function  named Calculate_Factorial.
    This function should do the following:
    1. accept a single integer 'n' as input.
    2. calculate the factorial 'n!'.
    3. Include a clear docstring explaining what the function does.
    4. Handle edge cases: the factorial of 0 is 1.
    5. Handle invalid input (e.g., non-integer values or negative numbers) by raising a ValueError with an appropriate message.
    """
    current_code = ""  # Nothing yet

    # the reflection loop
    max_iterations = 3
    message_history = [HumanMessage(content=task_prompt)]
    for i in range(max_iterations):
        logging.info(f"Reflection iteration {i + 1}/{max_iterations} ...")
        # 1. Generate the initial response
        if i == 0:
            response = llm.invoke(message_history)
        else:
            # Message history now includes the task, last code, and the last critique,
            # so we instruct the model to follow the critique
            message_history.append(HumanMessage(content="Please revise the code based on the critique provided."))
            response = llm.invoke(message_history)
            current_code = response.content

        message_history.append(response)

        # 2. Reflect stage
        reflector_prompt = [
            SystemMessage(
                content="""
                You are a senior software engineer and an expert in Python. Your role is to perform a meticulous code review.
                          Critically evaluate the provided Python code based on the original task requirements.
                          Look for bugs, style issues, missing edge cases, and areas of improvement.
                          If the code is perfect and meets all the requirements, respond with 'CODE_IS_PERFECT'.
                          Otherwise, provide a bulleted list of your critiques.
                """
            ),
            HumanMessage(
                content=f"""
                Original task: {task_prompt}
                Here is the code to review:
                {current_code}
                """
            ),
        ]

        critique_response = llm.invoke(reflector_prompt)
        critique = critique_response.content

        logging.info("Critique:\n" + critique)

        # 3. Check if the critique indicates the code is perfect
        if "CODE_IS_PERFECT" in critique:
            logging.info("Code is perfect. Ending reflection loop.")
            break

        # Add the critique to the message history for the next iteration
        message_history.append(HumanMessage(content=critique))

    logging.info("Final code after reflection loop:\n" + response.content)


if __name__ == "__main__":
    run_reflection_loop()
