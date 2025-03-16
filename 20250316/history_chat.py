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

# ✅ 여러 프롬프트 템플릿을 딕셔너리로 관리
prompts = {
    "default": ChatPromptTemplate.from_messages([
        ("system", "당신은 도움이 되는 AI 비서입니다. 사용자의 질문에 한국어로 친절하게 답변하고, 이전 대화 내용을 기억하여 맥락에 맞는 응답을 제공합니다."),
        ("placeholder", "{history}"),
        ("human", "{input}")
    ]),
    "casual": ChatPromptTemplate.from_messages([
        ("system", "당신은 친근한 말투로 대화하는 AI 챗봇입니다. 편안한 분위기로 응답하세요."),
        ("placeholder", "{history}"),
        ("human", "{input}")
    ]),
    "technical": ChatPromptTemplate.from_messages([
        ("system", "당신은 전문적인 AI 도우미입니다. 기술적인 질문에 대해 자세하고 정확한 답변을 제공합니다."),
        ("placeholder", "{history}"),
        ("human", "{input}")
    ])
}

# 대화 체인 저장소
chains = {name: prompt | llm for name, prompt in prompts.items()}

# 세션별 대화 기록 저장소
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    """세션별 대화 기록을 저장하고 관리"""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# ✅ 세션별로 다른 프롬프트를 사용할 수 있도록 설정
def process_conversation(user_input, session_id, prompt_name="default"):
    """사용자가 선택한 프롬프트로 대화 진행"""
    if prompt_name not in chains:
        return f"오류: '{prompt_name}' 프롬프트가 존재하지 않습니다."

    conversation_chain = RunnableWithMessageHistory(
        chains[prompt_name],
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )

    try:
        response = conversation_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        return response.content
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

# 세션 기록 삭제 함수
def clear_session(session_id):
    if session_id in store:
        del store[session_id]
        return f"세션 {session_id}의 대화 기록이 삭제되었습니다."
    return f"세션 {session_id}를 찾을 수 없습니다."

# ✅ 대화 테스트 (프롬프트 선택 가능)
if __name__ == "__main__":
    session_id = "user_session_1"

    print("사용할 프롬프트를 선택하세요: (default, casual, technical)")
    prompt_name = input("> ").strip()

    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        response = process_conversation(user_input, session_id, prompt_name)
        print(f"응답: {response}")
