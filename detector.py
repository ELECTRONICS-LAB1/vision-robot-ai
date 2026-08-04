import cv2
import numpy as np

from forma import detectar_forma
from color import detectar_color


def detectar_objeto(ruta_imagen):

    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        return None

    # ==========================================
    # PREPROCESAMIENTO
    # ==========================================

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    gris = cv2.GaussianBlur(gris, (5, 5), 0)

    _, binaria = cv2.threshold(
        gris,
        120,
        255,
        cv2.THRESH_BINARY_INV
    )

    kernel = np.ones((3, 3), np.uint8)

    binaria = cv2.morphologyEx(
        binaria,
        cv2.MORPH_OPEN,
        kernel
    )

    binaria = cv2.morphologyEx(
        binaria,
        cv2.MORPH_CLOSE,
        kernel
    )

    # ==========================================
    # CONTORNOS
    # ==========================================

    contornos, _ = cv2.findContours(
        binaria,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contornos) == 0:
        return None

    contorno = max(contornos, key=cv2.contourArea)

    area = cv2.contourArea(contorno)

    if area < 300:
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
    # RECORTAR OBJETO
    # ==========================================

    x, y, w, h = cv2.boundingRect(contorno)

    margen = 10

    x = max(0, x - margen)
    y = max(0, y - margen)

    w = min(imagen.shape[1] - x, w + 2 * margen)
    h = min(imagen.shape[0] - y, h + 2 * margen)

    objeto = imagen[y:y+h, x:x+w]

    # ==========================================
    # DETECCIÓN
    # ==========================================

    color = detectar_color(objeto)

    forma = detectar_forma(objeto)

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
    print("OBJETO DETECTADO")
    print("----------------------------------")
    print("Color :", color)
    print("Forma :", forma)
    print("Area  :", area)
    print("Centro:", (cx, cy))
    print("----------------------------------")

    return resultado