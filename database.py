import sqlite3
from datetime import datetime

DB = "vision_robot.db"


# ==========================================
# CREAR BASE DE DATOS
# ==========================================

def crear_base():

    conexion = sqlite3.connect(DB)

    cursor = conexion.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS piezas(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            fecha TEXT,

            color TEXT,

            forma TEXT,

            x INTEGER,

            y INTEGER,

            area REAL

        )

    """)

    conexion.commit()

    conexion.close()

    print("Base de datos lista.")


# ==========================================
# GUARDAR PIEZA
# ==========================================

def guardar_pieza(color, forma, x, y, area):

    conexion = sqlite3.connect(DB)

    cursor = conexion.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""

        INSERT INTO piezas
        (fecha,color,forma,x,y,area)

        VALUES
        (?,?,?,?,?,?)

    """,(fecha,color,forma,x,y,area))

    conexion.commit()

    conexion.close()

    print("Pieza guardada correctamente.")


# ==========================================
# TOTAL DE PIEZAS
# ==========================================

def obtener_total():

    conexion = sqlite3.connect(DB)

    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM piezas")

    total = cursor.fetchone()[0]

    conexion.close()

    return total


# ==========================================
# CONTAR POR COLOR
# ==========================================

def contar_color(color):

    conexion = sqlite3.connect(DB)

    cursor = conexion.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM piezas WHERE color=?",

        (color,)

    )

    cantidad = cursor.fetchone()[0]

    conexion.close()

    return cantidad


# ==========================================
# ULTIMA PIEZA
# ==========================================

def obtener_ultima_pieza():

    conexion = sqlite3.connect(DB)

    cursor = conexion.cursor()

    cursor.execute("""

        SELECT color,forma,fecha

        FROM piezas

        ORDER BY id DESC

        LIMIT 1

    """)

    dato = cursor.fetchone()

    conexion.close()

    return dato


# ==========================================
# HISTORIAL
# ==========================================

def obtener_historial(limite=20):

    conexion = sqlite3.connect(DB)

    cursor = conexion.cursor()

    cursor.execute("""

        SELECT

        fecha,

        color,

        forma

        FROM piezas

        ORDER BY id DESC

        LIMIT ?

    """,(limite,))

    datos = cursor.fetchall()

    conexion.close()

    return datos
# ==========================================
# BORRAR TODA LA BASE
# ==========================================

def borrar_base():

    conexion = sqlite3.connect(DB)

    cursor = conexion.cursor()

    cursor.execute("DELETE FROM piezas")

    conexion.commit()

    conexion.close()

    print("Base de datos eliminada correctamente.")