from flask import Flask, render_template, request, redirect
import os 

from detector import detectar_objeto
from database import (
    crear_base,
    guardar_pieza,
    obtener_total,
    contar_color,
    obtener_ultima_pieza,
    obtener_historial,
    borrar_base
)

# ==========================================
# FLASK
# ==========================================

app = Flask(__name__)

crear_base()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Resultado para ESP32
ultimo_resultado = "ESPERANDO"

# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    datos = {

        "TOTAL": obtener_total(),

        "ROJO": contar_color("ROJO"),

        "AZUL": contar_color("AZUL"),

        "VERDE": contar_color("VERDE"),

        "AMARILLO": contar_color("AMARILLO"),

        "NEGRO": contar_color("NEGRO"),

        "BLANCO": contar_color("BLANCO")

    }

    ultima = obtener_ultima_pieza()

    historial = obtener_historial()

    return render_template(

        "dashboard.html",

        datos=datos,

        ultima=ultima,

        historial=historial

    )

# ==========================================
# PAGINA PRINCIPAL
# ==========================================

@app.route("/", methods=["GET", "POST"])
def inicio():

    global ultimo_resultado

    resultado = None

    if request.method == "POST":

        print("===== RECIBÍ UN POST =====")

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

        print("Imagen guardada:", ruta)

        try:

            datos = detectar_objeto(ruta)

            print("Resultado detector:", datos)

            if datos is None:

                resultado = "NO SE DETECTÓ NINGÚN OBJETO"

                ultimo_resultado = "ERROR"

            else:

                resultado = f'{datos["color"]},{datos["forma"]}'

                ultimo_resultado = resultado

                # =====================================
                # GUARDAR EN SQLITE
                # =====================================

                guardar_pieza(

                    datos["color"],

                    datos["forma"],

                    datos["x"],

                    datos["y"],

                    datos["area"]

                )

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
# LIMPIAR BASE
# ==========================================
@app.route("/limpiar")
def limpiar():

    print(">>> ENTRÉ A LIMPIAR <<<")

    borrar_base()

    return redirect("/dashboard")

# ==========================================
# INICIO
# ==========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )