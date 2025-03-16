import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()



# model 
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template(
    "You are an expert in astronomy. Answer the question. <Question>: {input}")
output_parser = StrOutputParser()


# chain 연결 (LCEL)
chain = prompt | llm | output_parser

# chain 호출
response = chain.invoke({"input": "지구의 자전 주기는?"})
print(response)