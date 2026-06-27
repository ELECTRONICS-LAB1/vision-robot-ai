import cv2
import numpy as np

def detectar_forma(imagen):

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
        return "DESCONOCIDA"

    contorno = max(contornos, key=cv2.contourArea)

    area = cv2.contourArea(contorno)

    if area < 500:
        return "DESCONOCIDA"

    perimetro = cv2.arcLength(contorno, True)

    aproximacion = cv2.approxPolyDP(
        contorno,
        0.02 * perimetro,
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

        return "RECTANGULO"

    elif lados > 8:

        area = cv2.contourArea(contorno)

        perimetro = cv2.arcLength(contorno, True)

        circularidad = (4 * np.pi * area) / (perimetro * perimetro)

        if circularidad > 0.80:
            return "CIRCULO"

        return "ESTRELLA"

    else:

        hull = cv2.convexHull(contorno)

        hull_area = cv2.contourArea(hull)

        if hull_area == 0:
            return "DESCONOCIDA"

        solidez = area / hull_area

        if solidez < 0.85:
            return "ESTRELLA"

    return "DESCONOCIDA"