# functions.py

import os
import random
import string
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import tkinter as tk
from tkinter import filedialog

def generate_random_key(length=16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_iv(length=16):
    return os.urandom(length)

def encrypt_file(file_path, key, iv):
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    cipher = Cipher(algorithms.AES(key.encode()), modes.CFB8(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext

def save_to_file(data, file_path):
    with open(file_path, 'wb') as file:
        file.write(data)

def load_key(key_file):
    key_data = key_file.read()
    return key_data

def decrypt_file(uploaded_file, key, iv):
    if not uploaded_file:
        return b''

    ciphertext = uploaded_file.read()

    cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext

def open_directory_dialog(title):
    root = tk.Tk()
    root.withdraw()

    folder_path = None

    def ask_directory():
        nonlocal folder_path
        folder_path = filedialog.askdirectory(title=title)
        root.quit()

    root.after(0, ask_directory)
    root.mainloop()

    if folder_path is not None:
        generate_and_save_key(folder_path)

    return folder_path

def generate_and_save_key(output_folder):
    key = generate_random_key()
    key_file_path = os.path.join(output_folder, "clave.txt")
    save_to_file(key.encode(), key_file_path)

    print(f"La clave se ha guardado en {key_file_path}")

    return key
