# 이 코드는 비트코인 스타일의 바이너리 트랜잭션 포맷을 구현합니다.
# 
# RLP 방식의 장점:
# 1. 표준화: 널리 사용되며, 관련 문서와 예제가 많아 학습에 용이함.
# 2. 간결함: 복잡한 체크섬 로직이 필요 없어 실수 가능성이 줄어듦.
# 3. 커뮤니티 지원: 문제 발생 시 도움을 받을 수 있는 자료가 많음.
#
# 체크섬 추가의 복잡성:
# 1. 복잡성 증가: 사용자 정의 포맷은 로직이 복잡해져 실수할 가능성이 높음.
# 2. 디버깅 어려움: 체크섬 오류 발생 시 원인 파악이 어려울 수 있음.
#
# 결론:
# - 프로젝트 목표와 범위에 맞춰 방법 선택.
# - 단순한 프로젝트에는 RLP 같은 표준 방식 사용 추천.
# - 복잡한 요구 시 사용자 정의 포맷 고려.
# - 항상 코드 리뷰와 테스트를 통해 안정성을 높임.


import struct
import hashlib

def double_sha256(data):
    """Double SHA256 해시 함수"""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def calculate_checksum(data):
    """체크섬 계산"""
    return double_sha256(data)[:4]

# 트랜잭션 필드 정의
nonce = 9                     # nonce: 트랜잭션 순서
gas_price = 20000000000       # gasPrice: 가스 가격
gas_limit = 21000             # gasLimit: 가스 제한
to_address = bytes.fromhex('1abcde1234567890abcdef1234567890abcdef12')  # 수신자 주소
value = 1000000000000000000    # 전송할 이더의 양 (1 이더)
data = b''                    # 데이터 필드

# 트랜잭션 바이너리 인코딩
tx_binary = struct.pack(
    '>I Q Q 20s Q I',  # 형식 정의: nonce, gasPrice, gasLimit, to, value, data 길이
    nonce, gas_price, gas_limit, to_address, value, len(data)
) + data  # 데이터 추가

# 체크섬 계산
checksum = calculate_checksum(tx_binary)

# 최종 바이너리 포맷
final_tx = tx_binary + checksum  # 체크섬 추가

# 인코딩된 결과 출력
print(f"바이너리 인코딩된 트랜잭션: {final_tx.hex()}")

# 체크섬 검증
recomputed_checksum = final_tx[-4:]  # 마지막 4바이트를 체크섬으로 사용
is_valid = recomputed_checksum == checksum
print(f"\n체크섬 검증 결과: {is_valid}")