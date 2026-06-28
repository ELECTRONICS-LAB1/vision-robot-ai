import cv2
import numpy as np


def detectar_forma(imagen):

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Suavizar conservando bordes
    gris = cv2.bilateralFilter(gris, 9, 75, 75)

    # Mejorar contraste
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gris = clahe.apply(gris)

    # Umbral adaptativo
    binaria = cv2.adaptiveThreshold(
        gris,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        8
    )

    # Eliminar ruido
    kernel = np.ones((3,3), np.uint8)

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

    contornos, _ = cv2.findContours(
        binaria,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contornos) == 0:
        return "DESCONOCIDA"

    contorno = max(contornos, key=cv2.contourArea)

    area = cv2.contourArea(contorno)

    if area < 800:
        return "DESCONOCIDA"

    perimetro = cv2.arcLength(contorno, True)

    aproximacion = cv2.approxPolyDP(
        contorno,
        0.018 * perimetro,
        True
    )

    lados = len(aproximacion)

    print("Lados:", lados)

    if lados == 3:
        return "TRIANGULO"

    elif lados == 4:

        x, y, w, h = cv2.boundingRect(aproximacion)

        relacion = w / float(h)

        if 0.90 <= relacion <= 1.10:
            return "CUADRADO"

        else:
            return "RECTANGULO"

    else:

        circularidad = (4 * np.pi * area) / (perimetro * perimetro)

        if circularidad > 0.83:
            return "CIRCULO"

        hull = cv2.convexHull(contorno)

        hull_area = cv2.contourArea(hull)

        if hull_area > 0:

            solidez = area / hull_area

            if solidez < 0.86:
                return "ESTRELLA"

        if 5 <= lados <= 8:
            return "POLIGONO"

    return "DESCONOCIDA"