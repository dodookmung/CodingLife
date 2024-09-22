# 이더리움에 사용되는 블록 인코딩 방식으로 모듈만 불러오면 매우 간편하나,
# 비트코인의 Base58Check 인코딩과 다르게 체크섬을 지원하지 않아, 노드간 전송 시 비트 플립 오류에 안전하지 않다.
#


import rlp
from rlp.sedes import big_endian_int, binary

# 이더리움 트랜잭션 필드 정의
class Transaction(rlp.Serializable):
    fields = [
        ('nonce', big_endian_int),           # nonce: 트랜잭션을 전송한 계정의 트랜잭션 순서
        ('gasPrice', big_endian_int),        # gasPrice: 트랜잭션 처리에 지불할 가스 비용
        ('gasLimit', big_endian_int),        # gasLimit: 트랜잭션에 할당할 최대 가스 양
        ('to', binary),                      # to: 수신자 주소
        ('value', big_endian_int),           # value: 전송할 이더의 양
        ('data', binary)                     # data: 스마트 컨트랙트 실행에 필요한 데이터
    ]

# 예시 트랜잭션 데이터
tx = Transaction(
    nonce=9,                                 # nonce 값
    gasPrice=20000000000,                    # gasPrice 값
    gasLimit=21000,                          # gasLimit 값
    to=b'\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35\x35',  # 수신자 주소
    value=1000000000000000000,               # value 값 (1 이더)
    data=b''                                 # 빈 데이터 필드
)

# 트랜잭션을 RLP로 인코딩
encoded_tx = rlp.encode(tx)

# 인코딩된 결과 출력
print(f"RLP 인코딩된 트랜잭션: {encoded_tx.hex()}")


print("\n"*3)


# RLP 디코딩
decoded_tx = rlp.decode(encoded_tx, Transaction)

# 디코딩된 트랜잭션 출력
print(f"디코딩된 트랜잭션: {decoded_tx}")
print(f"Nonce: {decoded_tx.nonce}")
print(f"GasPrice: {decoded_tx.gasPrice}")
print(f"GasLimit: {decoded_tx.gasLimit}")
print(f"To: {decoded_tx.to.hex()}")
print(f"Value: {decoded_tx.value}")
print(f"Data: {decoded_tx.data.hex()}")