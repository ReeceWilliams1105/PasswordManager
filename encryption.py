from cryptography.fernet import Fernet
from settings import service_name
import bcrypt
import keyring

def set_master_key():
    keyring.set_password(service_name, service_name, bcrypt("password"))

def generate_key():
    """Generate a new Fernet key."""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """Load the Fernet key from a file."""
    return open("key.key", "rb").read()

def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()