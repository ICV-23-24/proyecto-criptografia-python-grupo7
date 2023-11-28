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

def encrypt_file(uploaded_file, key, iv, output_folder):
    # Verificar si se proporcionó un archivo
    if not uploaded_file:
        return b''  # Devolver una cadena vacía si no hay archivo

    plaintext = uploaded_file.read()

    cipher = Cipher(algorithms.AES(key.encode()), modes.CFB8(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Guardar el archivo cifrado en la carpeta especificada
    encrypted_file_path = os.path.join(output_folder, "archivo_cifrado.txt")
    save_to_file(ciphertext, encrypted_file_path)

    print(f"El archivo cifrado se ha guardado en {encrypted_file_path}")

def save_to_file(data, file_path):
    with open(file_path, 'wb') as file:
        file.write(data)

def encrypt_message(message, key, iv):
    cipher = Cipher(algorithms.AES(key.encode()), modes.CFB8(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return ciphertext

def decrypt_message(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key.encode()), modes.CFB8(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

def load_key(key_file_path):
    with open(key_file_path, 'rb') as key_file:
        return key_file.read()

def decrypt_file(uploaded_file, key, iv):
    # Verificar si se proporcionó un archivo
    if not uploaded_file:
        return b''  # Devolver una cadena vacía si no hay archivo

    ciphertext = uploaded_file.read()

    cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext

def open_file_dialog(title, filetypes):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return file_path

def open_directory_dialog(title):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title=title)
    return folder_path
