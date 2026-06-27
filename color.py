import cv2
import numpy as np


def detectar_color(imagen):

    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    colores = {

        "ROJO": [
            ((0, 120, 70), (10, 255, 255)),
            ((170, 120, 70), (180, 255, 255))
        ],

        "AZUL": [
            ((100, 120, 70), (130, 255, 255))
        ],

        "VERDE": [
            ((40, 70, 70), (85, 255, 255))
        ],

        "AMARILLO": [
            ((20, 120, 120), (35, 255, 255))
        ],

        "NEGRO": [
            ((0, 0, 0), (180, 255, 40))
        ],

        "BLANCO": [
            ((0, 0, 180), (180, 40, 255))
        ]

    }

    mejor_color = "DESCONOCIDO"
    mayor_area = 0

    for nombre, rangos in colores.items():

        area_total = 0

        for bajo, alto in rangos:

            mascara = cv2.inRange(
                hsv,
                np.array(bajo),
                np.array(alto)
            )

            # Ignorar los píxeles negros creados por la máscara
            if nombre != "NEGRO":

                mascara = cv2.bitwise_and(
                    mascara,
                    cv2.inRange(
                        hsv,
                        np.array((0, 0, 20)),
                        np.array((180, 255, 255))
                    )
                )

            area_total += cv2.countNonZero(mascara)

        if area_total > mayor_area:

            mayor_area = area_total
            mejor_color = nombre

    return mejor_color