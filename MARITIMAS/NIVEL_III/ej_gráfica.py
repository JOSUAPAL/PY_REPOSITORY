# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 05:21:42 2024
Ejemplo para graficar animada una funcion
@author: JOSUAPAL
"""

#---------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Definir los parámetros de las distribuciones normales
mean_x1, std_dev_x1 = 1.97, 0.125
mean_x2, std_dev_x2 = 5, 1.20

# Generar 100 muestras aleatorias para X1 y X2
samples_x1 = np.random.normal(mean_x1, std_dev_x1, 100)
samples_x2 = np.random.normal(mean_x2, std_dev_x2, 100)

# Crear la figura y el eje
fig, ax = plt.subplots()
scatter = ax.scatter([], [], alpha=0.7, label='Muestras Aleatorias')
line_x1 = ax.axvline(x=mean_x1, color='b', linestyle='--', label=f'Media X1: {mean_x1}')
line_x2 = ax.axhline(y=mean_x2, color='r', linestyle='--', label=f'Media X2: {mean_x2}')

# Establecer los límites de los ejes X e Y
ax.set_xlim(1, 3)
ax.set_ylim(0, 10)

# Etiquetas y leyenda
ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.legend()
ax.set_title('Animación de Pruebas Aleatorias de Variables X1 y X2')

# Función de inicialización
def init():
    scatter.set_offsets(np.column_stack(([], [])))
    return scatter,

# Función de actualización para la animación
def update(frame):
    x1 = samples_x1[:frame]
    x2 = samples_x2[:frame]
    scatter.set_offsets(np.column_stack((x1, x2)))
    return scatter,

# Crear la animación con control de velocidad
num_frames = len(samples_x1)
# Ajusta el valor de interval para controlar la velocidad de la animación
ani = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, interval=100)

# Mostrar la animación
plt.show()

#---------------------------------
