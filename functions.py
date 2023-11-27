from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
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

def encrypt_file(uploaded_file, key, iv):
    # Verificar si se proporcionó un archivo
    if not uploaded_file:
        return b''  # Devolver una cadena vacía si no hay archivo

    plaintext = uploaded_file.read()

    cipher = Cipher(algorithms.AES(key.encode()), modes.CFB8(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext

def save_to_file(data, file_path):
    with open(file_path, 'wb') as file:
        file.write(data)

def encrypt_message(message, key, iv):
    cipher = Cipher(algorithms.AES(key.encode()), modes.CFB8(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return ciphertext

def decrypt_message(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

def load_key(key_file_path):
    with open(key_file_path, 'rb') as key_file:
        return key_file.read()

def decrypt_file(uploaded_file, key, iv):
    # Verificar si se proporcionó un archivo
    if not uploaded_file:
        return ''

    ciphertext = uploaded_file.read()

    cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext

def main():
    root = tk.Tk()
    root.withdraw()  # Evita que se abra la ventana principal de tkinter

    # Abrir el explorador de archivos para seleccionar un archivo cifrado
    encrypted_file_path = filedialog.askopenfilename(title="Selecciona un archivo cifrado", filetypes=[("Text files", "*.txt")])

    if not encrypted_file_path:
        print("No se seleccionó ningún archivo cifrado. Saliendo.")
        return

    # Abrir el explorador de archivos para seleccionar un archivo con la clave
    key_file_path = filedialog.askopenfilename(title="Selecciona un archivo con la clave", filetypes=[("Text files", "*.txt")])

    if not key_file_path:
        print("No se seleccionó ningún archivo con la clave. Saliendo.")
        return

    # Cargar la clave desde el archivo
    encryption_key = load_key(key_file_path)

    # Abrir el explorador de archivos para seleccionar la carpeta de destino
    output_folder = filedialog.askdirectory(title="Selecciona la carpeta de destino para el archivo descifrado")

    if not output_folder:
        print("No se seleccionó ninguna carpeta de destino. Saliendo.")
        return

    # Generar un vector de inicialización aleatorio de 16 bytes
    iv = os.urandom(16)

    # Descifrar el archivo seleccionado
    decrypted_data = decrypt_file(encrypted_file_path, encryption_key, iv)

    # Guardar el archivo descifrado en la carpeta especificada
    decrypted_file_path = os.path.join(output_folder, "archivo_descifrado.txt")
    save_to_file(decrypted_data, decrypted_file_path)

    print(f"El archivo desencriptado se ha guardado en {decrypted_file_path}")

if __name__ == "__main__":
    main()
