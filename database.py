import sqlite3

from encryption import decrypt_password, encrypt_password, load_key;

def create_database():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_password(service, username, password):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    key = load_key()
    encrypted_password = encrypt_password(password, key)
    cursor.execute('INSERT INTO passwords (service_name, username, password) VALUES (?, ?, ?)', (service, username, encrypted_password))
    conn.commit()
    conn.close()

def retrieve_password(service, username):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    key = load_key()
    cursor.execute('SELECT password FROM passwords WHERE service_name = ? AND username = ?', (service, username))
    result = cursor.fetchone()
    conn.close()
    if result:
        return decrypt_password(result[0], key)
    return None

def update_password(service, username, new_password):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    key = load_key()
    encrypted_password = encrypt_password(new_password, key)
    cursor.execute('UPDATE passwords SET password = ? WHERE service_name = ? AND username = ?', (encrypted_password, service, username))
    conn.commit()
    conn.close()

def delete_password(service, username):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE service_name = ? AND username = ?', (service, username))
    conn.commit()
    conn.close()