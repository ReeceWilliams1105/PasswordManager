from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
import argon2.low_level as a2ll

"""Internal use function which generates the encryption key to be used for the Fernet key
    Utilised argon2 low level fixed length key generation to conform to AES length requirements, whilst maintaining security of masterKey"""
def derive_key_argon2(password, salt):
    return a2ll.hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=4,
        memory_cost=65536,
        parallelism=2,
        hash_len=32,
        type=a2ll.Type.ID
    )

"""Encrypts the fernet key utilising AES with the key generated using a generated hash of the 
    users master password."""
def encrypt_fernet_key_argon2(fernet_key, password):
    salt = os.urandom(16)
    key = derive_key_argon2(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Pad fernet_key to 32 bytes for AES block size
    pad_len = 16 - (len(fernet_key) % 16)
    padded_key = fernet_key + bytes([pad_len] * pad_len)
    encrypted = encryptor.update(padded_key) + encryptor.finalize()
    # Store salt and iv with encrypted key
    return base64.b64encode(salt + iv + encrypted)

"""Decrypts the Fernet key, required the encrypted string and the users master password, which is the seed
    for the AES encryption key."""
def decrypt_fernet_key_argon2(encrypted_data, password):
    data = base64.b64decode(encrypted_data)
    salt = data[:16]
    """Initialisation vector"""
    iv = data[16:32]
    encrypted = data[32:]
    key = derive_key_argon2(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_key = decryptor.update(encrypted) + decryptor.finalize()
    pad_len = padded_key[-1]
    return padded_key[:-pad_len]