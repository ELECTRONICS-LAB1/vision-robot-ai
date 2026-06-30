import cv2
import numpy as np


def detectar_forma(contorno):

    area = cv2.contourArea(contorno)

    if area < 800:
        return "DESCONOCIDA"

    perimetro = cv2.arcLength(contorno, True)

    if perimetro == 0:
        return "DESCONOCIDA"

    aproximacion = cv2.approxPolyDP(
        contorno,
        0.03 * perimetro,
        True
    )

    lados = len(aproximacion)

    print("--------------------------------")
    print("Área:", area)
    print("Perímetro:", perimetro)
    print("Lados:", lados)

    # ==========================
    # TRIÁNGULO
    # ==========================

    if lados == 3:
        return "TRIANGULO"

    # ==========================
    # CUADRADO
    # ==========================

    elif lados == 4:

        x, y, w, h = cv2.boundingRect(aproximacion)

        relacion = w / float(h)

        print("Relación:", relacion)

        if 0.85 <= relacion <= 1.15:
            return "CUADRADO"

        return "DESCONOCIDA"

    # ==========================
    # CÍRCULO
    # ==========================

    circularidad = (4 * np.pi * area) / (perimetro * perimetro)

    print("Circularidad:", circularidad)

    if circularidad >= 0.80:
        return "CIRCULO"

    return "DESCONOCIDA"