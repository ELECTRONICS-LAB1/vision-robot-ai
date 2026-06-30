import cv2
import numpy as np


def detectar_forma(imagen):

    # ==========================
    # ESCALA DE GRISES
    # ==========================

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Suavizar conservando bordes
    gris = cv2.bilateralFilter(gris, 9, 75, 75)

    # Mejorar contraste
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    gris = clahe.apply(gris)

    # ==========================
    # BINARIZACIÓN
    # ==========================

    binaria = cv2.adaptiveThreshold(

        gris,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY_INV,

        31,

        8

    )

    # ==========================
    # LIMPIEZA
    # ==========================

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

    # ==========================
    # CONTORNOS
    # ==========================

    contornos, _ = cv2.findContours(

        binaria,

        cv2.RETR_EXTERNAL,

        cv2.CHAIN_APPROX_SIMPLE

    )

    if len(contornos) == 0:

        return "DESCONOCIDA"

    contorno = max(contornos, key=cv2.contourArea)

    area = cv2.contourArea(contorno)

    print("Área:", area)

    if area < 800:

        return "DESCONOCIDA"

    # ==========================
    # APROXIMACIÓN
    # ==========================

    perimetro = cv2.arcLength(contorno, True)

    aproximacion = cv2.approxPolyDP(

        contorno,

        0.02 * perimetro,

        True

    )

    lados = len(aproximacion)

    print("Lados detectados:", lados)

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

        else:

            return "DESCONOCIDA"

    # ==========================
    # CÍRCULO
    # ==========================

    else:

        circularidad = (4 * np.pi * area) / (perimetro * perimetro)

        print("Circularidad:", circularidad)

        if circularidad >= 0.80:

            return "CIRCULO"

    # ==========================
    # NO RECONOCIDA
    # ==========================

    return "DESCONOCIDA"