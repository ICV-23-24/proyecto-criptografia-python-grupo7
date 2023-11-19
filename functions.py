# Librerías
# Cifrado Simétrico
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
# Gestión de ficheros Flask
import os
from werkzeug.utils import secure_filename

# Variables globales 
carpeta_ficheros='data/ficheros'
carpeta_ficheros_encriptados='data/ficheros_encriptados'
carpeta_claves='data/claves_simetricas'

# Cifrado Simétrico
# Encriptación AES
def encrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return b64encode(encrypted_message).decode('utf-8')

# Desencriptación AES
def decrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(b64decode(message)), AES.block_size).decode('utf-8')
    return decrypted_message

# Gestión de ficheros Flask
# Subida de archivos
def subir_archivo(archivo):
    # Comprobamos con secure_filename de que el archivo no contenga caracteres no seguros.
    nombre_archivo=secure_filename(archivo.filename)
    # Almacenamos el archivo en Flask con la librería OS
    archivo.save(os.path.join(carpeta_ficheros, nombre_archivo))
    # Obtenemos la ruta del archivo almacenado en string para otras funciones
    ruta_archivo=carpeta_ficheros+nombre_archivo
    return ruta_archivo