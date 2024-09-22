import hashlib
import base58

def double_sha256(data):
    """Double SHA256 해시 함수"""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def base58check_encode(payload):
    """Base58Check 인코딩 함수"""
    # 1. 버전 바이트 추가 (예: 0x00 for mainnet 비트코인 주소)
    version_byte = b'\x00' + payload
    # 2. 체크섬 계산
    checksum = double_sha256(version_byte)[:4]
    # 3. 버전 + 데이터 + 체크섬 결합
    versioned_payload = version_byte + checksum
    # 4. Base58 인코딩
    return base58.b58encode(versioned_payload)

# 비트코인 주소로 사용할 공개 키 해시 (예시)
public_key_hash = bytes.fromhex('1abcde1234567890abcdef1234567890abcdef12')

# Base58Check 인코딩 수행
address = base58check_encode(public_key_hash)

print(f"Base58Check 인코딩된 주소: {address.decode()}")