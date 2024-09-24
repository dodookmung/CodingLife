import hashlib
import time
import json
from typing import List, Tuple

# 상수 정의
VERSION = 1
GENESIS_TIMESTAMP = 1231006505
GENESIS_MERKLE_ROOT = bytes.fromhex("4a5e1e4baa6e1d6e7cdd9fd2554988911e834f04fcb20192e4b27b3766c8342e")
BLOCKCHAIN_FILE = "blockchain.json"


def double_sha256(data: bytes) -> bytes:
    """SHA-256 해시를 두 번 적용하여 결과를 반환합니다."""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def int_to_little_endian(value: int, length: int) -> bytes:
    """정수를 리틀 엔디안 바이트로 변환합니다."""
    return value.to_bytes(length, 'little')


def create_merkle_root(transactions: List[bytes]) -> bytes:
    """트랜잭션 리스트를 받아 Merkle Root를 생성합니다."""
    if not transactions:
        return bytes(32)  # 빈 트랜잭션일 경우 0으로 채워진 Merkle Root 반환
    elif len(transactions) == 1:
        return double_sha256(transactions[0])
    else:
        new_level = []
        for i in range(0, len(transactions), 2):
            left = transactions[i]
            right = transactions[i + 1] if i + 1 < len(transactions) else left
            new_level.append(double_sha256(left + right))
        return create_merkle_root(new_level)


def create_genesis_block() -> Tuple[str, int]:
    """제네시스 블록을 생성하고 해시와 타임스탬프를 반환합니다."""
    prev_block_hash = 0  # 이전 블록 해시는 0으로 설정 (Genesis 블록)
    
    # 블록 헤더 구성
    block_header = (
        int_to_little_endian(VERSION, 4) +
        int_to_little_endian(prev_block_hash, 32) +  # 제네시스 블록이므로 이전 블록은 0
        GENESIS_MERKLE_ROOT[::-1] +  # Merkle Root (리틀 엔디안)
        int_to_little_endian(GENESIS_TIMESTAMP, 4)
    )

    # 블록 해시 계산 (SHA-256 두 번 적용)
    block_hash = double_sha256(block_header)[::-1]
    return block_hash.hex(), GENESIS_TIMESTAMP


def create_new_block(prev_block_hash: str, transactions: List[bytes]) -> Tuple[str, int]:
    """이전 블록 해시를 참조하여 새로운 블록을 생성합니다."""
    merkle_root = create_merkle_root(transactions)  # 새로운 트랜잭션 기반으로 Merkle Root 생성
    timestamp = int(time.time())  # 현재 시간을 타임스탬프로 사용

    # 블록 헤더 구성 (이전 블록의 해시를 포함)
    block_header = (
        int_to_little_endian(VERSION, 4) +
        bytes.fromhex(prev_block_hash) +  # 이전 블록 해시
        merkle_root[::-1] +
        int_to_little_endian(timestamp, 4)
    )

    # 새로운 블록의 해시 계산 (SHA-256 두 번 적용)
    block_hash = double_sha256(block_header)[::-1]
    return block_hash.hex(), timestamp


def save_blockchain_to_file(blockchain: List[str]) -> None:
    """블록체인 데이터를 파일에 저장합니다."""
    with open(BLOCKCHAIN_FILE, 'w') as f:
        json.dump(blockchain, f)


def generate_blocks(block_interval: int = 1) -> None:
    """블록체인 생성 및 블록 연결을 수행합니다."""
    blockchain = []

    # Genesis 블록 생성
    genesis_block_hash, _ = create_genesis_block()
    print(f"Genesis Block Hash: {genesis_block_hash}")

    # 블록체인에 제네시스 블록 추가
    blockchain.append(genesis_block_hash)
    save_blockchain_to_file(blockchain)  # 초기 블록체인 저장

    # 다음 블록을 주기적으로 생성
    while True:
        transactions = [b'transaction_1', b'transaction_2']  # 실제 트랜잭션으로 대체 가능
        
        prev_block_hash = blockchain[-1]
        new_block_hash, new_timestamp = create_new_block(prev_block_hash, transactions)
        print(f"New Block Hash: {new_block_hash} (Timestamp: {new_timestamp})")
        
        blockchain.append(new_block_hash)
        save_blockchain_to_file(blockchain)  # 블록체인 파일에 저장
        time.sleep(block_interval)  # 블록 생성 간격

# 블록 생성 실행
generate_blocks()
