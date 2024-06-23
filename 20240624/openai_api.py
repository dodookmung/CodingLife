from openai import OpenAI

import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "너는 나에게 도움을 주는 챗봇이야"},
    {"role": "user", "content": "안녕? 오늘 기분은 어떠니?"}
  ]
)

print(completion.choices[0].message)

# output:
#ChatCompletionMessage(content='안녕하세요! 제 기분은 좋아요, 도와드릴 일이 있나요?', role='assistant', function_call=None, tool_calls=None)