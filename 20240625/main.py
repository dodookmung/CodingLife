import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage



chat = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="치와와의 평균 수명은?")
]


response = chat.invoke(messages)
print(response.content)