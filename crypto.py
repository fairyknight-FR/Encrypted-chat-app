from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Pre-shared key (must be SAME in client & server)
KEY = b'12345678901234567890123456789012'  # 32 bytes = AES-256

def encrypt_message(message: str) -> bytes:
    aesgcm = AESGCM(KEY)
    nonce = os.urandom(12)  # Secure IV
    ciphertext = aesgcm.encrypt(nonce, message.encode(), None)
    return nonce + ciphertext  # send nonce + encrypted data

def decrypt_message(data: bytes) -> str:
    aesgcm = AESGCM(KEY)
    nonce = data[:12]
    ciphertext = data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None).decode()
