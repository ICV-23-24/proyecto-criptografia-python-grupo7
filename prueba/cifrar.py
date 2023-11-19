import os
import tkinter as tk
from tkinter import filedialog
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import random
import string

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

def main():
    root = tk.Tk()
    root.withdraw()  # Evita que se abra la ventana principal de tkinter

    # Abrir el explorador de archivos para seleccionar un documento de texto
    file_path = filedialog.askopenfilename(title="Selecciona un archivo de texto", filetypes=[("Text files", "*.txt")])

    if not file_path:
        print("No se seleccionó ningún archivo. Saliendo.")
        return

    # Abrir el explorador de archivos para seleccionar la carpeta de destino
    output_folder = filedialog.askdirectory(title="Selecciona la carpeta de destino")

    if not output_folder:
        print("No se seleccionó ninguna carpeta de destino. Saliendo.")
        return

    # Generar una clave aleatoria de 16 bytes (128 bits)
    encryption_key = generate_random_key()

    # Generar un vector de inicialización aleatorio de 16 bytes
    iv = generate_random_iv()

    # Cifrar el archivo seleccionado
    encrypted_data = encrypt_file(file_path, encryption_key, iv)

    # Guardar el archivo cifrado en la carpeta especificada
    encrypted_file_path = os.path.join(output_folder, "archivo_cifrado.txt")
    save_to_file(encrypted_data, encrypted_file_path)

    # Guardar la clave en un archivo
    key_file_path = os.path.join(output_folder, "clave.txt")
    save_to_file(encryption_key.encode(), key_file_path)

    print(f"Archivo cifrado guardado en {encrypted_file_path}")
    print(f"Clave guardada en {key_file_path}")

if __name__ == "__main__":
    main()