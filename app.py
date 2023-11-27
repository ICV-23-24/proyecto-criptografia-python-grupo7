from datetime import datetime
from flask import Flask, render_template, request, jsonify
from functions import generate_random_key, generate_random_iv, encrypt_file, decrypt_file

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/csimetrico/", methods=['GET', 'POST'])
def csimetrico():
    if request.method == 'POST':
        mode = request.form['mode']

        if mode == 'encrypt':
            # Obtener el archivo del formulario
            uploaded_file = request.files['file']

            # Realizar las operaciones necesarias con el archivo, por ejemplo:
            key = generate_random_key()
            iv = generate_random_iv()
            encrypted_data = encrypt_file(uploaded_file, key, iv)

            # Devolver una respuesta, puedes ajustar según tus necesidades
            return jsonify({"result": "success", "message": "Encriptado completado"})

        elif mode == 'decrypt':
            # Obtener el archivo del formulario
            uploaded_file = request.files['file']

            # Realizar las operaciones necesarias con el archivo, por ejemplo:
            key = generate_random_key()
            iv = generate_random_iv()
            decrypted_data = decrypt_file(uploaded_file, key, iv)

            # Devolver una respuesta, puedes ajustar según tus necesidades
            return jsonify({"result": "success", "message": "Desencriptado completado"})

    return render_template("csimetrico.html")

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/doc/")
def doc():
    return render_template("doc.html")

@app.route("/otro/")
def otro():
    return render_template("otro.html")



@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")