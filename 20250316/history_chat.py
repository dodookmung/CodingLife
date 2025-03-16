import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

# 모델 초기화 - API 키 검증 추가
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

# 모델 초기화 - 온도 매개변수 추가하여 응답 일관성 향상
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 프롬프트 템플릿 개선 - 시스템 메시지를 더 상세하게 작성
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 도움이 되는 AI 비서입니다. 사용자의 질문에 한국어로 친절하게 답변하고, 이전 대화 내용을 기억하여 맥락에 맞는 응답을 제공합니다."),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

# 대화 체인 생성
chain = prompt | llm

# 세션별 대화 기록 저장소 관리
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    """세션별 대화 기록을 저장하고 관리"""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 대화 기록 관리 체인 생성
conversation_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# 에러 처리 함수 추가
def process_conversation(user_input, session_id):
    try:
        response = conversation_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        return response
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"


# 대화 시뮬레이션
session_id = "user_session_1"

while True:
    user_input = input("> ")
    response = process_conversation(user_input, session_id)
    print(f"응답: {response.content}")

# 메모리 정리 함수 추가
def clear_session(session_id):
    if session_id in store:
        del store[session_id]
        return f"세션 {session_id}의 대화 기록이 삭제되었습니다."
    return f"세션 {session_id}를 찾을 수 없습니다."

# 사용 예시
# clear_session("user_session_1")