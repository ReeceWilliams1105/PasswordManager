from cryptography.fernet import Fernet
from settings import service_name
from keyDerivation import encrypt_fernet_key_argon2, derive_key_argon2, decrypt_fernet_key_argon2
import argon2 as a2
import keyring

ph = a2.PasswordHasher()

"""Set the masterKey in the keyring on the local system using a salted bcrypt password."""
def set_master_key(masterPassword):
    hash = ph.hash(masterPassword)
    keyring.set_password(service_name, service_name, hash)
    if keyring.get_password((service_name+"fernet"), (service_name+"fernet")) == None:
        print("here!")
        generate_fernet_key(masterPassword)

"""Checks the masterKey by encoding and comparing against the stored salted hash in the keyring."""
def check_masterKey(masterPassword):
    hash = keyring.get_password(service_name, service_name).encode('utf-8')
    try:
        ph.verify(hash, masterPassword)
        if ph.check_needs_rehash(hash):
            keyring.set_password(service_name, service_name, ph.hash(masterPassword)) 
        return True
    except:
        return False

"""Generates the fernet key for use in encrypting individual service passwords.
    Encrypts the key using the KDF process and AES for storage in the system keyring.
    The encryption key is the hashed version of the Master password."""
def generate_fernet_key(mpw):
    key = Fernet.generate_key()
    encryptedKey = encrypt_fernet_key_argon2(key, mpw)
    keyring.set_password((service_name+"fernet"), (service_name+"fernet"), encryptedKey)

"""Loads the decrypted fernet key using the master password of the user."""
def load_key(mpw):
    return decrypt_fernet_key_argon2(keyring.get_password((service_name+"fernet"), (service_name+"fernet")), mpw)

def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()