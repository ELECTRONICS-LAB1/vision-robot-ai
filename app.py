from flask import Flask, render_template, request
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

# ==========================================
# CARGAR API KEY
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("No se encontró GEMINI_API_KEY en el archivo .env")

client = genai.Client(api_key=API_KEY)

# ==========================================
# FLASK
# ==========================================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Estado que leerá la ESP32
ultimo_color = "ESPERANDO"

# ==========================================
# PAGINA PRINCIPAL
# ==========================================

@app.route("/", methods=["GET", "POST"])
def inicio():

    global ultimo_color

    resultado = None

    if request.method == "POST":

        archivo = request.files["imagen"]

        if archivo.filename == "":
            return render_template(
                "index.html",
                resultado="No se seleccionó imagen."
            )

        ruta = os.path.join(
            UPLOAD_FOLDER,
            archivo.filename
        )

        archivo.save(ruta)

        # Tipo MIME
        extension = ruta.lower()

        if extension.endswith(".png"):
            mime = "image/png"
        elif extension.endswith(".jpeg"):
            mime = "image/jpeg"
        else:
            mime = "image/jpeg"

        with open(ruta, "rb") as f:
            imagen = f.read()

        respuesta = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=[

                """
Analiza únicamente el objeto principal.

Responde SOLO con UNA palabra.

Opciones:

ROJO
AZUL
VERDE
AMARILLO
NEGRO
BLANCO

No escribas ninguna explicación.
""",

                types.Part.from_bytes(
                    data=imagen,
                    mime_type=mime
                )

            ]
        )

        resultado = respuesta.text.strip().upper()

        ultimo_color = resultado

        print("--------------------------------")
        print("COLOR DETECTADO:", ultimo_color)
        print("--------------------------------")

    return render_template(
        "index.html",
        resultado=resultado
    )

# ==========================================
# CONSULTA DE LA ESP32
# ==========================================

@app.route("/resultado")
def resultado():

    global ultimo_color

    color = ultimo_color

    # Después de leerlo vuelve a esperar
    ultimo_color = "ESPERANDO"

    return color

# ==========================================
# SABER SI EL SERVIDOR ESTA VIVO
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