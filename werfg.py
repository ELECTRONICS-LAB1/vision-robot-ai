import numpy as np
import matplotlib.pyplot as plt

# ===================================================
# INVERSOR MONOFASICO DE ONDA CUADRADA
# Carga puramente resistiva
# ===================================================

# Datos
Vdc = 125          # Voltios
R = 25             # Ohmios
f = 60             # Hz

# Parámetros
I = Vdc / R
T = 1 / f

# Tiempo (2 periodos)
t = np.linspace(0, 2*T, 2000)

# ---------------------------------------------------
# Voltaje de salida
# ---------------------------------------------------

vo = np.where((t % T) < T/2, Vdc, -Vdc)

# ---------------------------------------------------
# Corriente en la carga
# ---------------------------------------------------

io = np.where((t % T) < T/2, I, -I)

# ---------------------------------------------------
# Corriente en S1 y S4
# ---------------------------------------------------

iS14 = np.where((t % T) < T/2, I, 0)

# ---------------------------------------------------
# Corriente en S2 y S3
# ---------------------------------------------------

iS23 = np.where((t % T) >= T/2, I, 0)

# ---------------------------------------------------
# Corriente de la fuente
# ---------------------------------------------------

iFuente = np.ones_like(t)*I

# ===================================================
# GRAFICAS
# ===================================================

plt.figure(figsize=(11,12))

# Voltaje
plt.subplot(5,1,1)
plt.plot(t*1000, vo, linewidth=2)
plt.grid(True)
plt.ylabel("Voltaje (V)")
plt.title("Voltaje de salida")
plt.ylim([-150,150])

# Corriente carga
plt.subplot(5,1,2)
plt.plot(t*1000, io, linewidth=2)
plt.grid(True)
plt.ylabel("Corriente (A)")
plt.title("Corriente en la carga")
plt.ylim([-6,6])

# Interruptores S1-S4
plt.subplot(5,1,3)
plt.plot(t*1000, iS14, linewidth=2)
plt.grid(True)
plt.ylabel("Corriente (A)")
plt.title("Corriente en S1 y S4")
plt.ylim([-1,6])

# Interruptores S2-S3
plt.subplot(5,1,4)
plt.plot(t*1000, iS23, linewidth=2)
plt.grid(True)
plt.ylabel("Corriente (A)")
plt.title("Corriente en S2 y S3")
plt.ylim([-1,6])

# Fuente
plt.subplot(5,1,5)
plt.plot(t*1000, iFuente, linewidth=2)
plt.grid(True)
plt.ylabel("Corriente (A)")
plt.xlabel("Tiempo (ms)")
plt.title("Corriente de la fuente")
plt.ylim([-1,6])

plt.tight_layout()
plt.show()

# ===================================================
# RESULTADOS
# ===================================================

I_med_carga = 0
I_rms_carga = I

I_med_fuente = I
I_rms_fuente = I

I_med_sw = I/2
I_rms_sw = I/np.sqrt(2)

print("============== RESULTADOS ==============")
print(f"Corriente de carga = {I:.2f} A")
print(f"Valor medio carga = {I_med_carga:.2f} A")
print(f"Valor eficaz carga = {I_rms_carga:.2f} A")

print("----------------------------------------")
print(f"Valor medio fuente = {I_med_fuente:.2f} A")
print(f"Valor eficaz fuente = {I_rms_fuente:.2f} A")

print("----------------------------------------")
print(f"Valor medio S1 = {I_med_sw:.2f} A")
print(f"Valor eficaz S1 = {I_rms_sw:.2f} A")

print("----------------------------------------")
print(f"Valor medio S2 = {I_med_sw:.2f} A")
print(f"Valor eficaz S2 = {I_rms_sw:.2f} A")

print("----------------------------------------")
print(f"Valor medio S3 = {I_med_sw:.2f} A")
print(f"Valor eficaz S3 = {I_rms_sw:.2f} A")

print("----------------------------------------")
print(f"Valor medio S4 = {I_med_sw:.2f} A")
print(f"Valor eficaz S4 = {I_rms_sw:.2f} A")