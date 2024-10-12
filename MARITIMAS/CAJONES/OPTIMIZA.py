# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 19:42:50 2024

@author: PC-JSUAREZ
"""
import numpy as np
from scipy.optimize import minimize
import ezdxf

# Longitudes de las paredes
L1 = 250  # Longitud de la pared 1
L2 = 323  # Longitud de la pared 2
rodapie_ancho = 20  # Ancho del rodapié

# Restricciones de longitud del rodapié y de las juntas
max_L = 60  # Máxima longitud del rodapié
min_d = 0.50  # Mínima separación entre rodapiés
max_d = 1.20  # Máxima separación entre rodapiés

# Definimos la función objetivo: maximizar la longitud L de los rodapiés
def objective(x):
    L = x[0]  # Longitud del rodapié
    return -L  # Queremos maximizar L, por eso devolvemos el negativo

# Definimos las restricciones del problema
def constraint1(x):
    L = x[0]  # Longitud del rodapié
    d1 = x[1]  # Juntas para la pared 1
    d2 = x[2]  # Juntas para la pared 2
    
    # Ajustamos la longitud disponible en las paredes debido al ancho del rodapié en la esquina
    available_L1 = L1 - rodapie_ancho  # Longitud restante en la pared 1
    available_L2 = L2 - rodapie_ancho  # Longitud restante en la pared 2
    
    # Número de rodapiés en cada pared (debe ser un número entero)
    n1 = np.floor(available_L1 / (L + d1))
    n2 = np.floor(available_L2 / (L + d2))
    
    # Longitud total cubierta por los rodapiés y las juntas
    total1 = n1 * L + (n1 - 1) * d1
    total2 = n2 * L + (n2 - 1) * d2
    
    # Queremos que el total cubra exactamente la longitud de las paredes
    return [total1 - available_L1, total2 - available_L2]

# Restricciones de las juntas y longitud del rodapié
cons = [{'type': 'eq', 'fun': lambda x: constraint1(x)[0]},  # Pared 1
        {'type': 'eq', 'fun': lambda x: constraint1(x)[1]}]  # Pared 2

# Restricciones de las variables (bounds)
bounds = [(0.5, max_L), (min_d, max_d), (min_d, max_d)]  # (L, d1, d2)

# Condiciones iniciales (inicializamos cerca de los valores límites)
x0 = [max_L, min_d, min_d]

# Optimización
result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

# Resultados
L_optimo = result.x[0]
d1_optimo = result.x[1]
d2_optimo = result.x[2]

print("Longitud óptima del rodapié (L):", L_optimo)
print("Juntas para la pared 1 (d1):", d1_optimo)
print("Juntas para la pared 2 (d2):", d2_optimo)
print("Longitud máxima alcanzada:", -result.fun)

# --- Generación del archivo DXF ---

# Crear un nuevo archivo DXF
doc = ezdxf.new(dxfversion="R2010")
msp = doc.modelspace()

# Dibujar los rodapiés en la pared 1
x_start = 0  # Iniciamos en el origen
n1 = int(np.floor((L1 - rodapie_ancho) / (L_optimo + d1_optimo)))  # Número de rodapiés en pared 1
for i in range(n1):
    # Dibujar cada rodapié
    msp.add_line((x_start, 0), (x_start + L_optimo, 0))
    x_start += L_optimo + d1_optimo

# Dibujar los rodapiés en la pared 2 (en ángulo de 90 grados)
y_start = 0
n2 = int(np.floor((L2 - rodapie_ancho) / (L_optimo + d2_optimo)))  # Número de rodapiés en pared 2
for i in range(n2):
    # Dibujar cada rodapié
    msp.add_line((0, y_start), (0, y_start + L_optimo))
    y_start += L_optimo + d2_optimo

# Guardar el archivo DXF
doc.saveas("rodapies_optimizados.dxf")

print("Archivo DXF generado: rodapies_optimizados.dxf")


