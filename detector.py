import cv2
import numpy as np

from forma import detectar_forma
from color import detectar_color


def detectar_objeto(ruta_imagen):

    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        return None

    # ==========================================
    # BUSCAR EL OBJETO
    # ==========================================

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    gris = cv2.GaussianBlur(gris, (5, 5), 0)

    _, binaria = cv2.threshold(
        gris,
        180,
        255,
        cv2.THRESH_BINARY_INV
    )

    contornos, _ = cv2.findContours(
        binaria,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contornos) == 0:
        return None

    contorno = max(contornos, key=cv2.contourArea)

    area = cv2.contourArea(contorno)

    if area < 500:
        return None

    # ==========================================
    # CENTRO DEL OBJETO
    # ==========================================

    M = cv2.moments(contorno)

    if M["m00"] != 0:

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

    else:

        cx = 0
        cy = 0

    # ==========================================
    # CREAR MASCARA DEL OBJETO
    # ==========================================

    mascara = np.zeros(imagen.shape[:2], dtype=np.uint8)

    cv2.drawContours(
        mascara,
        [contorno],
        -1,
        255,
        -1
    )

    objeto = cv2.bitwise_and(
        imagen,
        imagen,
        mask=mascara
    )

    # ==========================================
    # RECORTAR SOLO EL OBJETO
    # ==========================================

    x, y, w, h = cv2.boundingRect(contorno)

    objeto = objeto[y:y+h, x:x+w]

    # ==========================================
    # DETECTAR FORMA
    # ==========================================

    forma = detectar_forma(imagen)

    # ==========================================
    # DETECTAR COLOR
    # ==========================================

    color = detectar_color(objeto)

    # ==========================================
    # RESULTADO
    # ==========================================

    resultado = {

        "color": color,

        "forma": forma,

        "x": cx,

        "y": cy,

        "area": area

    }

    print("----------------------------------")
    print(resultado)
    print("----------------------------------")

    return resultado