import hashlib
import struct
import time

# SHA-256 해시를 두 번 적용하는 함수
def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

# 리틀 엔디안으로 변환하는 유틸리티 함수
def int_to_little_endian(value, length):
    return value.to_bytes(length, 'little')

# Genesis 블록의 코인베이스 트랜잭션 생성 함수
def create_coinbase_tx():
    coinbase_message = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
    coinbase_script = bytes(coinbase_message, 'utf-8')
    
    # 트랜잭션의 해시를 두 번 적용 (임시로 매우 간단하게 표현)
    tx_hash = double_sha256(coinbase_script)
    return tx_hash

# Genesis 블록의 헤더 구성 함수
def create_genesis_block():
    version = 1  # 블록 버전
    prev_block = 0  # 이전 블록 해시 (Genesis 블록은 0)
    merkle_root = create_coinbase_tx()  # 코인베이스 트랜잭션으로부터 Merkle Root 계산
    timestamp = 1231006505  # 2009년 1월 3일
    bits = 0x1d00ffff  # 난이도 목표
    nonce = 2083236893  # 채굴된 논스 값
    
    # 블록 헤더를 리틀 엔디안 형식으로 구성
    block_header = (
        int_to_little_endian(version, 4) +
        int_to_little_endian(prev_block, 32) +
        merkle_root[::-1] +  # Merkle Root는 바이트 순서가 반대로 저장됨
        int_to_little_endian(timestamp, 4) +
        int_to_little_endian(bits, 4) +
        int_to_little_endian(nonce, 4)
    )

    # 블록 해시 계산 (SHA-256 두 번 적용)
    block_hash = double_sha256(block_header)[::-1]  # 해시를 다시 리틀 엔디안 형식으로 변환

    return block_hash.hex()

# Genesis 블록 해시 출력
genesis_block_hash = create_genesis_block()
print(f"Genesis Block Hash: {genesis_block_hash}")
