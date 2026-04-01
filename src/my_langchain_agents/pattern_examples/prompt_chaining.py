"""Sample Prompt chaining patterns."""

from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

# Requires an OpenAI API key to be set in the environment
llm = ChatOpenAI(model="gpt-4.1", temperature=0)

# Prompt 1: Extract information
prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{input_text}"
)

# Prompt 2: Transform to JSON
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following technical specifications into JSON object with 'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
)

# Build the chain using LCEL
extraction_chain = prompt_extract | llm | StrOutputParser()

full_chain: Runnable[Any, Any] = {"specifications": extraction_chain} | prompt_transform | llm | StrOutputParser()

# Run the chain
input_text = """The new laptop has an Intel i7 processor, 16GB of RAM, and a 512GB SSD."""
result = full_chain.invoke({"input_text": input_text})

print(result)
