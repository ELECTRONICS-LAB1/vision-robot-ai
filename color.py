import cv2
import numpy as np


def detectar_color(imagen):

    # Convertir a HSV
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # ==========================
    # RANGOS HSV
    # ==========================

    colores = {

        "ROJO": [
            ((0, 70, 50), (15, 255, 255)),
            ((165, 70, 50), (180, 255, 255))
        ],

        "AZUL": [
            ((95, 100, 50), (130, 255, 255))
        ],

        "VERDE": [
            ((40, 80, 40), (85, 255, 255))
        ],

        "BLANCO": [
            ((0, 0, 180), (180, 40, 255))
        ]

    }

    kernel = np.ones((5, 5), np.uint8)

    mejor_color = "DESCONOCIDO"
    mayor_area = 0

    for nombre, rangos in colores.items():

        area_total = 0

        for bajo, alto in rangos:

            mascara = cv2.inRange(
                hsv,
                np.array(bajo, dtype=np.uint8),
                np.array(alto, dtype=np.uint8)
            )

            # Eliminar ruido
            mascara = cv2.morphologyEx(
                mascara,
                cv2.MORPH_OPEN,
                kernel
            )

            mascara = cv2.morphologyEx(
                mascara,
                cv2.MORPH_CLOSE,
                kernel
            )

            # Ignorar el fondo negro
            fondo = cv2.inRange(
                hsv,
                np.array((0, 0, 25), dtype=np.uint8),
                np.array((180, 255, 255), dtype=np.uint8)
            )

            mascara = cv2.bitwise_and(
                mascara,
                fondo
            )

            area_total += cv2.countNonZero(mascara)

        print(nombre, area_total)

        if area_total > mayor_area:

            mayor_area = area_total
            mejor_color = nombre

    if mayor_area < 100:

        return "DESCONOCIDO"

    print("----------------------------------")
    print("Color detectado:", mejor_color)
    print("Área:", mayor_area)
    print("----------------------------------")

    return mejor_color