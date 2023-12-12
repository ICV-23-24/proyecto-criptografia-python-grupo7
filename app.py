###################
#####LIBRERÍAS#####
###################
# app.py

import os
from flask import Flask, render_template, request, redirect, url_for
import funciones.functions as f
import funciones.functions_samba as fsmb
import funciones.functions_flask as fflask

app = Flask(__name__)

# Ruta principal
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        fflask.borrar_credencial()
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET', 'POST'])
def csimetrico():
    if request.method == 'POST':
        modo = request.form['modo']
        archivo = request.files['archivo']
        algoritmo = request.form['algoritmo']

        # Lógica para el encriptado
        if modo == 'encriptacion':
            almacenamiento = request.form['almacenamiento']

            if algoritmo == 'AES':
                key = f.generate_random_key()
                iv = f.generate_random_iv()

                # Solicitar al usuario la carpeta de destino y encriptar el archivo
                output_folder = f.open_directory_dialog("Selecciona la carpeta de destino para el archivo cifrado")
                f.encrypt_file(archivo, key, iv, output_folder)

                return render_template("csimetrico.html", result="Operación de encriptación exitosa")

            elif algoritmo == 'DES':
                # Lógica para DES
                pass  # Debes proporcionar la lógica para DES aquí

            # Almacenamiento
            if almacenamiento == 'local':
                # Lógica para almacenamiento local
                pass  # Debes proporcionar la lógica para almacenamiento local aquí
            elif almacenamiento == 'compartida':
                # Lógica para almacenamiento compartido
                pass  # Debes proporcionar la lógica para almacenamiento compartido aquí

        # Lógica para desencriptado
        elif modo == 'desencriptacion':
            clave = request.files['clave']
            if algoritmo == 'AES':
                key = f.load_key(clave)
                iv = f.generate_random_iv()

                print(f"Decrypted Key: {key.decode()}")
                decrypted_data = f.decrypt_file(archivo, key, iv)

                print(decrypted_data)

                # Solicitar al usuario la carpeta de destino y guardar el archivo descifrado
                output_folder = f.open_directory_dialog("Selecciona la carpeta de destino para el archivo descifrado")
                f.save_to_file(decrypted_data, os.path.join(output_folder, "archivo_descifrado.txt"))

                return render_template("csimetrico.html", result="Operación de desencriptación exitosa")

    return render_template("csimetrico.html")

if __name__ == "__main__":
    app.run(debug=True)

# ALGORITMO ASIMÉTRICO
@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")

# ALGORITMO HÍBRIDO
@app.route("/chibrido/")
def chibrido():
    return render_template("chibrido.html")

# LISTADO DE LOS ARCHIVOS COMPARTIDOS
@app.route("/listadoArchivos/", methods=['POST','GET'])
def listar_archivos():
        cookie=fflask.leer_credencial() # Comprobar si hay credencial almacenada

        if cookie==True: # Si hay credencial almacenada
            usuario,password,recurso_compartido=fflask.extraer_credencial() # Se extrae y se utiliza
            conexion=fsmb.conexion_smb(usuario,password) # Se realiza la conexión
            fsmb.listar_archivos_smb(recurso_compartido,conexion) # Se lista los archivos
            
            if request.method=='POST': # El usuario elige descargar un archivo
                nombre_archivo=request.form['nombre_archivo'] # Se obtiene el nombre del archivo seleccionado
                ruta_archivo_remoto=request.form['ruta_archivo_remoto'] # Se obtiene la ruta remota del archivo seleccionado
                
                conexion=fsmb.conexion_smb(usuario,password) # Se realiza la conexión
                ruta_archivo_descargado=fsmb.bajar_archivo_smb(nombre_archivo,ruta_archivo_remoto,recurso_compartido,conexion) # Se baja el archivo a la aplición
                return fflask.bajar_archivo(ruta_archivo_descargado) # Se envía el archivo al cliente
            
            return render_template("listado_archivos.html")
        
        elif cookie==False:
            if request.method=='POST': # El usuario inicia sesión
                usuario=request.form['usuario'] # Usuario para iniciar sesión en el servidor
                password=request.form['password'] # Contraseña para iniciar sesión en el servidor
                recurso_compartido=request.form['carpeta_compartida'] # Carpeta compartida en el servidor
                
                fflask.escribir_credencial(usuario,password,recurso_compartido) # Una vez introducidas la credencial se guarda para futuros inicios
                
                return render_template("listado_archivos.html")
        return render_template("login.html") # Pagina de inicio de sesión para el servidor remoto

# SOBRE EL EQUIPO
@app.route("/about/")
def about():
    return render_template("about.html")

# DOCUMENTACIÓN DEL PROYECTO
@app.route("/doc/")
def doc():
    return render_template("doc.html")

# DATOS DE LA API
@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")