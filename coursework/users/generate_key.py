from encryption_util import generate_key, save_key

key = generate_key()
save_key(key, 'encryption_key.key')
print("Ключ шифрування успішно створено і збережено в 'encryption_key.key'")
