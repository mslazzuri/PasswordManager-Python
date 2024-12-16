from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os
import base64
import bcrypt

SALT_LENGTH = 16  # Bytes
KEY_LENGTH = 32   # Bytes
ITERATIONS = 100000

# Generate a key from a password
def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt a password using AES-GCM
def encrypt_password(password: str) -> str:
    salt = os.urandom(SALT_LENGTH)
    key = generate_key("master_password", salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # GCM nonce is 12 bytes
    encrypted = aesgcm.encrypt(nonce, password.encode(), None)
    return base64.urlsafe_b64encode(salt + nonce + encrypted).decode()

# Decrypt a password using AES-GCM
def decrypt_password(encrypted_data: str) -> str:
    decoded = base64.urlsafe_b64decode(encrypted_data.encode())
    salt = decoded[:SALT_LENGTH]
    nonce = decoded[SALT_LENGTH:SALT_LENGTH + 12]
    encrypted = decoded[SALT_LENGTH + 12:]
    key = generate_key("master_password", salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, encrypted, None).decode()

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())