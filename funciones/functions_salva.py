from Cryptodome.Cipher import DES
from random import sample
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

ruta_keyrings="data/keyring"
ruta_archivo="data/archivos"

#GENERADOR DE CLAVES
# Declaramos la función con un argumento (longitud de la contraseña)
def generador_claves():
    longitud=8
 
    # Definimos los caracteres y simbolos
    
    abc_minusculas = "abcdefghijklmnopqrstuvwxyz"
    
    # upper() transforma las letras de una cadena en mayusculas
    abc_mayusculas = abc_minusculas.upper() 
    
    numeros = "0123456789"
    simbolos = "{}[]()*;/,_-"
    
    # Definimos la secuencia
    secuencia = abc_minusculas + abc_mayusculas + numeros + simbolos
    
    # Llamamos la función sample() utilizando la secuencia, y la longitud
    password_union = sample(secuencia, longitud)
    
    # Con join insertamos los elementos de una lista en una cadena
    password_result = "".join(password_union)
    
    # Retornamos la variables "password_result"
    return password_result

def cifrado(ruta_archivo, key):
    # Definir rutas para el archivo encriptado y la clave
    ruta_archivo_encriptado = ruta_archivo + '.enc'
    ruta_archivo_clave = ruta_archivo + '.des'
    nombre_archivo_encriptado = ruta_archivo_encriptado[14:]
    nombre_archivo_clave = ruta_archivo_clave[14:]

    # Leer el contenido del archivo en modo binario
    with open(ruta_archivo, 'rb') as archivo:
        plaintext = archivo.read()

    # Codificar la clave a bytes
    keyenc = key.encode()

    # Crear un objeto de cifrado DES en modo OFB (Output Feedback)
    cipher = DES.new(keyenc, DES.MODE_OFB)

    # Cifrar el texto plano y agregar el vector de inicialización (IV)
    msg = cipher.iv + cipher.encrypt(plaintext)

    # Escribir el mensaje cifrado en un nuevo archivo
    with open(ruta_archivo_encriptado, 'wb') as archivo:
        archivo.write(msg)

    # Escribir la clave en un archivo separado
    with open(ruta_archivo_clave, 'w') as archivo:
        archivo.write(key)

    # Devolver las rutas de los archivos encriptados y la clave
    return ruta_archivo_encriptado,ruta_archivo_clave,nombre_archivo_encriptado,nombre_archivo_clave

def descifrado(ruta_archivo_encriptado, ruta_archivo_clave):
    # Crear la ruta para el archivo desencriptado
    ruta_archivo_desencriptado = ruta_archivo_encriptado[:-4] + '.desenc'
    print(ruta_archivo_desencriptado)

    # Leer el mensaje encriptado desde el archivo
    with open(ruta_archivo_encriptado, 'rb') as archivo:
        msg = archivo.read()

    # Leer la clave desde el archivo
    with open(ruta_archivo_clave, 'r') as archivo:
        key = archivo.read()

    # Codificar la clave a bytes
    keyenc = key.encode()

    # Obtener el vector de inicialización (IV) del mensaje cifrado
    iv = msg[:8]

    # Crear un objeto de cifrado DES en modo OFB (Output Feedback) con el IV
    cipher = DES.new(keyenc, DES.MODE_OFB, iv=iv)

    # Descifrar el texto cifrado (excluyendo el IV)
    decrypted_text = cipher.decrypt(msg[8:])

    # Escribir el texto descifrado en un nuevo archivo
    with open(ruta_archivo_desencriptado, 'wb') as archivo:
        archivo.write(decrypted_text)

    # Devolver la ruta del archivo descifrado
    return ruta_archivo_desencriptado


def generar_claves_rsa(nombre_real):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    nombre_archivo_publica=nombre_real+".pem"
    # Guardar las claves en archivos
    clave_publica=ruta_keyrings+"/"+nombre_archivo_publica
    clave_privada=ruta_keyrings+"/"+nombre_real+".key"

    with open(clave_privada, "wb") as private_file:
        private_file.write(private_key)

    with open(clave_publica, "wb") as public_file:
        public_file.write(public_key)
    return clave_privada,clave_publica,nombre_archivo_publica

def cifrar_rsa(archivo_original,nombre_archivo_original,ruta_clave_publica):
    
    clave_publica = open(ruta_clave_publica, "rb").read()

    key = RSA.import_key(clave_publica)
    cipher = PKCS1_OAEP.new(key)
    
    with open(archivo_original, "rb") as file:
        data = file.read()
        ciphertext = cipher.encrypt(data)

    nombre_archivo_encriptado=nombre_archivo_original+'.enc'
    archivo_cifrado=ruta_archivo+"/"+nombre_archivo_encriptado
    ruta_archivo_encriptado = archivo_cifrado

    with open(archivo_cifrado, "wb") as file:
        file.write(ciphertext)
        return ruta_archivo_encriptado,nombre_archivo_encriptado

def descifrar_rsa(archivo_cifrado,ruta_clave_privada):
    
    clave_privada = open(ruta_clave_privada, "rb").read()
    
    ruta_archivo_desencriptado_rsa = archivo_cifrado[:-4] + '.desenc'
    key = RSA.import_key(clave_privada)
    cipher = PKCS1_OAEP.new(key)
    
    with open(archivo_cifrado, "rb") as file:
        ciphertext = file.read()
        decrypted_data = cipher.decrypt(ciphertext)
    
    with open(ruta_archivo_desencriptado_rsa, "wb") as file:
        file.write(decrypted_data)
    return ruta_archivo_desencriptado_rsa