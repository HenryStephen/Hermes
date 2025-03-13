"""
Chat models and prompts: Build a simple LLM application with prompt templates and chat models.
Reference: https://python.langchain.com/docs/tutorials/llm_chain/
"""
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from Hermes_utils.common_utils import CommonUtils

# 0. Load config
config = CommonUtils.get_sys_config()

# 1. Using Language Models
llm_model = ChatOllama(
    model=config["ollama"]["model"],
    temperature=config["ollama"]["temperature"],
)
messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]

# 1.1 messages invoking
response = llm_model.invoke(messages)
print(response)
print(type(response))  # <class 'langchain_core.messages.ai.AIMessage'>

# 1.2 other ways to invoke
print(llm_model.invoke("Hello"))
print(llm_model.invoke([{"role": "user", "content": "Hello"}]))
print(llm_model.invoke([HumanMessage("Hello")]))

# 1.3 streaming ways
for token in llm_model.stream(messages):
    print(token.content, end="|")

# 2. Prompt Templates
print("*" * 100)
system_template = "Translate the following from English into {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

# 2.1 the input to this prompt template is a dictionary.
prompt = prompt_template.invoke({"language": "Italian", "text": "hi!"})
print(prompt)

# 2.2 access the messages directly
print(prompt.to_messages())

# 2.3 invoke the chat model
response = llm_model.invoke(prompt)
print(response.content)
