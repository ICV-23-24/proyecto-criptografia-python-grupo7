# Librerías
# Aplicación
from datetime import datetime
from flask import Flask, render_template, request
# Funciones
import functions as f

app = Flask(__name__)


# Raíz del proyecto
@app.route("/")
def home():
    return render_template("home.html")

# Cifrado simétrico
@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    if request.method == 'POST':
        # Obtenemos del html los valores necesarios
        archivo=request.files['archivo']
        algoritmo=request.form['algoritmo']
        almacenamiento=request.form['almacenamiento']

        # Guardamos el archivo subido en la aplicación y obtenemos la ruta donde se ubica
        ruta_archivo=f.subir_archivo(archivo)
        return render_template("csimetrico.html")
    return render_template("csimetrico.html")

# Cifrado Asimétrico
@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")

# Cifrado Híbrido
@app.route("/chibrido/")
def chibrido():
    return render_template("chibrido.html")

# Sobre el equipo
@app.route("/about/")
def about():
    return render_template("about.html")

# Documentación del proyecto
@app.route("/doc/")
def doc():
    return render_template("doc.html")

# Listado de los archivos tanto local como compartido
@app.route("/listadoArchivos")
def listar_archivos():
    return render_template("listadoArchivos.html")

# Datos de la api
@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

# @app.route("/otro/")
# def otro():
#     return render_template("otro.html")

# Página hello
# @app.route("/hello/")
# @app.route("/hello/<name>")
# def hello_there(name = None):
#     return render_template(
#         "hello_there.html",
#         name=name,
#         date=datetime.now()
#     )