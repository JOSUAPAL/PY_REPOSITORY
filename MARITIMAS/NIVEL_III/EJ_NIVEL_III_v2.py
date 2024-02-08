# -*- coding: utf-8 -*-
"""
Created on Feb 8 08:21:42 2024
Ejemplo para graficar animada una funcion NIVEL III
@author: JOSUE
"""

#---------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Definir los parámetros de las distribuciones normales
mean_x1, std_dev_x1 = 1.97, 0.125
mean_x2, std_dev_x2 = 5, 1.20

N=10000
speed=0.00001

# Generar 100 muestras aleatorias para X1 y X2
samples_x1 = np.random.normal(mean_x1, std_dev_x1, N)
samples_x2 = np.random.normal(mean_x2, std_dev_x2, N)

# Crear la figura y los ejes para el primer plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Primer plot (animación de puntos)
scatter = ax1.scatter([], [], alpha=0.7, s=6, label='')  # blueucir tamaño de los puntos y quitar etiqueta
#line_x1 = ax1.axvline(x=mean_x1, color='b', linestyle='--', label='')  # Quitar etiqueta
#line_x2 = ax1.axhline(y=mean_x2, color='r', linestyle='--', label='')  # Quitar etiqueta

# Ecuación X2 = 3.325 * X1
def calculate_x2_line(x1_values):
    return 3.325 * x1_values

# Línea para representar X2 = 3.325 * X1
x1_line_values = np.linspace(1, 3, 100)
line_x2_equation, = ax1.plot(x1_line_values, calculate_x2_line(x1_line_values), color='r', linestyle='--', label='Estado límite')

# Establecer los límites de los ejes X e Y
ax1.set_xlim(1, 3)
ax1.set_ylim(0, 10)

# Agregar grid minor
ax1.grid(which='both', linestyle=':', linewidth='0.5', color='black', alpha=0.5)

# Etiquetas y leyenda
ax1.set_xlabel('X1')
ax1.set_ylabel('X2')

# Añadir puntos en la leyenda con la mitad de tamaño
legend_acierto = ax1.scatter([], [], color='blue', marker='o', s=3, label='Acierto')
legend_fallo = ax1.scatter([], [], color='red', marker='o', s=3, label='Fallo')
ax1.legend(handles=[legend_acierto, legend_fallo], loc='upper left')

# Título para el conteo de puntos
title_text = ax1.text(2.8, 0.1, '', fontsize=10, ha='right', va='bottom')
ax1.set_title('Nivel III. Simulaciones de Montecarlo')  # Inicializar el título

# Función de inicialización
def init():
    scatter.set_offsets(np.column_stack(([], [])))
    title_text.set_text('')
    return scatter, line_x2_equation, title_text, legend_acierto, legend_fallo

# Función de actualización para la animación
def update(frame):
    x1 = samples_x1[:frame]
    x2 = samples_x2[:frame]
    scatter.set_offsets(np.column_stack((x1, x2)))

    # Actualizar la línea de X2 = 3.325 * X1
    line_x2_equation.set_ydata(calculate_x2_line(x1_line_values))

    # Asignar colores en función de la condición 3.325 * X1 - X2 < 0
    colors = np.where(3.325 * x1 - x2 < 0, 'red', 'blue')
    scatter.set_facecolor(colors)

    # Actualizar el título con el conteo de puntos
    title_text.set_text(f'nº simulaciones: {frame}')

    # Actualizar leyenda de aciertos y fallos
    aciertos = np.sum(3.325 * x1 - x2 >= 0)
    fallos = np.sum(3.325 * x1 - x2 < 0)
    legend_acierto.set_offsets([[0, 0]])  # Solo para mostrar el punto en la leyenda
    legend_fallo.set_offsets([[0, 0]])  # Solo para mostrar el punto en la leyenda

    # Detener la animación al finalizar las muestras
    if frame == len(samples_x1) - 1:
        ani1.event_source.stop()

    return scatter, line_x2_equation, title_text, legend_acierto, legend_fallo

# Crear la animación con control de velocidad
num_frames = len(samples_x1)
# Ajusta el valor de interval para controlar la velocidad de la animación
ani1 = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, interval=speed)

# Segundo plot (animación de proporción de puntos azules)
red_proportion_line, = ax2.plot([], [], color='red', label='')
ax2.set_xlim(0, num_frames)
ax2.set_ylim(0, 0.5)  # Limitar el eje y entre 0 y 0.5
ax2.set_xlabel('Simulaciones')
ax2.set_ylabel('Probabilidad de fallo')
ax2.legend()

# Título para el conteo de proporción (ubicado en la parte inferior derecha)
title_text2 = ax2.text(0.95, 0.05, '', fontsize=10, ha='right', va='bottom', transform=ax2.transAxes)
ax2.set_title('Probabilidad de fallo')  # Inicializar el título

# Agregar grid minor
ax2.grid(which='both', linestyle=':', linewidth='0.5', color='black', alpha=0.5)

# Listas para almacenar el historial de la proporción de puntos azules
frame_history = []
proportion_history = []

# Función de inicialización para el segundo plot
def init2():
    red_proportion_line.set_data([], [])
    title_text2.set_text('')
    return red_proportion_line, title_text2

# Función de actualización para el segundo plot
def update2(frame):
    # Calcular la proporción de puntos azules respecto al total
    red_proportion = np.sum(3.325 * samples_x1[:frame] - samples_x2[:frame] < 0) / frame
    frame_history.append(frame)
    proportion_history.append(red_proportion)
    
    # Actualizar la línea de proporción
    red_proportion_line.set_data(frame_history, proportion_history)

    # Actualizar el título con el conteo de proporción (mostrar tres decimales)
    title_text2.set_text(f'Pf: {red_proportion:.3f}')

    # Detener la animación al finalizar las muestras
    if frame == len(samples_x1) - 1:
        ani2.event_source.stop()

    return red_proportion_line, title_text2

# Crear la animación con control de velocidad para el segundo plot
ani2 = FuncAnimation(fig, update2, frames=num_frames, init_func=init2, blit=True, interval=speed)

# Mostrar ambas animaciones
plt.show()
