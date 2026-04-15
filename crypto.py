from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

KEY = b'12345678901234567890123456789012'  # 32 bytes

def encrypt_message(message: str) -> bytes:
    aesgcm = AESGCM(KEY)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, message.encode(), None)
    return nonce + ciphertext

def decrypt_message(data: bytes) -> str:
    aesgcm = AESGCM(KEY)
    nonce = data[:12]
    ciphertext = data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None).decode()
