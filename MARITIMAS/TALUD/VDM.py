# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 20:59:33 2024

@author: PC-JSUAREZ
"""

import csv
import math

def VDM(Hc, Nod, Tm, Nolas, pmat, pw):
    # Cálculo de Som a partir de Tm
    Som = (2 * math.pi * Hc) / (9.81 * Tm ** 2)
    
    # Cálculo de Dn
    Dn = Hc / (((pmat / pw) - 1) * ((6.7 * ((Nod ** 0.4) / (Nolas ** 0.3)) + 1) * (Som ** -0.1)))
    
    # Cálculo de W
    W = (Dn ** 3) * pmat
    
    # Retornamos Dn y W
    return Dn, W

def procesar_csv(input_file, output_file):
    # Abrir archivo de entrada y salida
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='\t')
        fieldnames = ['CASOS', 'Dn', 'W']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
        
        # Escribir el encabezado en el archivo de salida
        writer.writeheader()
        
        # Procesar cada fila (caso)
        for row in reader:
            casos = row['CASOS']
            Hc = float(row['Hc'])
            Nod = float(row['Nod'])
            Tm = float(row['Tm'])
            Nolas = float(row['Nolas'])
            pmat = float(row['pmat'])
            pw = float(row['pw'])
            
            # Calcular Dn y W usando la función VDM
            Dn, W = VDM(Hc, Nod, Tm, Nolas, pmat, pw)
            
            # Escribir la fila de salida con los resultados
            writer.writerow({'CASOS': casos, 'Dn': round(Dn, 3), 'W': round(W, 3)})

# Definir la ruta de los archivos
input_file = 'input_VDM.csv'
output_file = 'Output_VDM.csv'

# Llamar a la función para procesar el archivo CSV
procesar_csv(input_file, output_file)


