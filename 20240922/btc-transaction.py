import hashlib
import base58

def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def base58check_encode(payload):
    version_byte = b'\x00' + payload
    checksum = double_sha256(version_byte)[:4]
    versioned_payload = version_byte + checksum
    return base58.b58encode(versioned_payload)

def create_transaction(sender, receiver, amount):
    transaction = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount
    }
    return transaction

# 유효한 비트코인 주소로 사용할 공개 키 해시
sender_public_key_hash = '1abcde1234567890abcdef1234567890abcdef12'
receiver_public_key_hash = 'abcdefabcdefabcdefabcdefabcdefabcdefabcdef'  # 40자리 16진수

# Base58Check 인코딩 수행
sender_address = base58check_encode(bytes.fromhex(sender_public_key_hash)).decode()
receiver_address = base58check_encode(bytes.fromhex(receiver_public_key_hash)).decode()

# 트랜잭션 생성
transaction = create_transaction(sender_address, receiver_address, 0.01)

print("트랜잭션 데이터:")
print(transaction)
print()
print(type(transaction))