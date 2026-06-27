from flask import Flask, render_template, request
import os

from detector import detectar_objeto

# ==========================================
# FLASK
# ==========================================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ultimo_resultado = "ESPERANDO"

# ==========================================
# PAGINA PRINCIPAL
# ==========================================

@app.route("/", methods=["GET", "POST"])
def inicio():

    global ultimo_resultado

    resultado = None

    if request.method == "POST":

        if "imagen" not in request.files:

            return render_template(
                "index.html",
                resultado="No se recibió ninguna imagen."
            )

        archivo = request.files["imagen"]

        if archivo.filename == "":

            return render_template(
                "index.html",
                resultado="No se seleccionó ninguna imagen."
            )

        ruta = os.path.join(
            UPLOAD_FOLDER,
            archivo.filename
        )

        archivo.save(ruta)

        try:

            datos = detectar_objeto(ruta)

            print("DATOS:", datos)

            if datos is None:

                resultado = "NO SE DETECTÓ NINGÚN OBJETO"

                ultimo_resultado = "ERROR"

            else:

                resultado = f'{datos["color"]},{datos["forma"]}'

                ultimo_resultado = resultado

                print("--------------------------------")
                print("COLOR :", datos["color"])
                print("FORMA :", datos["forma"])
                print("X :", datos["x"])
                print("Y :", datos["y"])
                print("AREA :", datos["area"])
                print("--------------------------------")

        except Exception as e:

            print("===================================")
            print("ERROR EN detector.py")
            print(e)
            print("===================================")

            resultado = f"ERROR: {e}"

    return render_template(
        "index.html",
        resultado=resultado
    )

# ==========================================
# CONSULTA ESP32
# ==========================================

@app.route("/resultado")
def resultado():

    global ultimo_resultado

    r = ultimo_resultado

    ultimo_resultado = "ESPERANDO"

    return r

# ==========================================
# ESTADO DEL SERVIDOR
# ==========================================

@app.route("/estado")
def estado():

    return "SERVIDOR OK"

# ==========================================
# INICIO
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )