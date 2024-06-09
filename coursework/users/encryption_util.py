from cryptography.fernet import Fernet

# Генерація ключа шифрування
def generate_key():
    return Fernet.generate_key()

# Збереження ключа в безпечному місці
def save_key(key, file_path):
    with open(file_path, 'wb') as key_file:
        key_file.write(key)

# Завантаження ключа
def load_key(file_path):
    with open(file_path, 'rb') as key_file:
        return key_file.read()

# Шифрування даних
def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

# Дешифрування даних
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data
