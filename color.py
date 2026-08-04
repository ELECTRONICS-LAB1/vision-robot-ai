import cv2
import numpy as np


def detectar_color(imagen):

    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    colores = {

        "ROJO": [

            ((0, 60, 40), (15, 255, 255)),
            ((165, 60, 40), (180, 255, 255))

        ],

        "VERDE": [

            ((40, 60, 40), (85, 255, 255))

        ],

        "AZUL": [

            ((95, 70, 40), (130, 255, 255))

        ],

        "BLANCO": [

            ((0, 0, 180), (180, 50, 255))

        ]

    }

    kernel = np.ones((3,3), np.uint8)

    mejor_color = "DESCONOCIDO"
    mayor_area = 0

    for nombre, rangos in colores.items():

        mascara_total = np.zeros(hsv.shape[:2], dtype=np.uint8)

        for bajo, alto in rangos:

            mascara = cv2.inRange(
                hsv,
                np.array(bajo, np.uint8),
                np.array(alto, np.uint8)
            )

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

            mascara_total = cv2.bitwise_or(
                mascara_total,
                mascara
            )

        area_total = cv2.countNonZero(mascara_total)

        # NO USAR EN RAILWAY
        # cv2.imshow(nombre, mascara_total)

        print(nombre, area_total)

        if area_total > mayor_area:

            mayor_area = area_total
            mejor_color = nombre

    print("--------------------------------")
    print("Mayor area:", mayor_area)
    print("Color:", mejor_color)
    print("--------------------------------")

    if mayor_area < 50:
        return "DESCONOCIDO"

    return mejor_color