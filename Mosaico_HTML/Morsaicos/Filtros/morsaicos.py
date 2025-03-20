"""
Proyecto final - Morsaicos.

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 1.5
"""

import os
from PIL import Image
import math

"""
Función que obtiene el color promedio de una región dada dentro 
de una imagen. 

Recibe la imagen, el punto de partida y las dimensiones de
la región.

Devuelve la tripleta RGB que define el color promedio de la región.
"""
def get_average_color(image, x, y, width, height):  
    pixels = image.load()
    total_r, total_g, total_b, count, a = 0, 0, 0, 0, 0    
    average_color = -1

    for i in range(x, min(x + width, image.width)):
        for j in range(y, min(y + height, image.height)):  #Se restringe el análisis al área              
        
            temp_r, temp_g, temp_b, a = pixels[i, j]  #Se procesan los valores rgb de cada pixel 
            total_r += temp_r                       
            total_g += temp_g
            total_b += temp_b
            count += 1

    if count == 0:
        average_color = 0        
    else:
        average_color = (total_r // count, total_g // count, total_b // count) #Tripleta con el color promedio
    
    return average_color


"""
Función que procesa una biblioteca de imágenes, una imagen a la vez,y obtiene
el color promedio de cada una de ellas. 

Recibe la ruta del directorio que contiene a la biblioteca junto con la ruta
para el archivo de salida.

Genera un .txt con la información obtenida del proceso.
"""
def save_average_colors(folder_path, output_file):    
    
    with open(output_file, "w") as f:
        
        for image_file in os.listdir(folder_path):
            if image_file.lower().endswith((".jpg", ".png")):
                image_path = os.path.join(folder_path, image_file)
                image = None
                
                with Image.open(image_path) as img:        
                    image = img.convert("RGBA")

                avg_color = get_average_color(image, 0, 0, image.width, image.height)                
                f.write(f"{image_file},{avg_color[0]},{avg_color[1]},{avg_color[2]}\n")                             
    

"""
Función que busca la imagen más cerca en términos del color promedio respecto
a un color de referencia. 

Recibe el color promedio de referencia, la ruta del archivo con la información
de aquellas imágenes entre las que se busca a una cercana, un factor númerico para
reducir la repetición de imágenes, así como un entero que indica que tipo de medida 
se emplea para dterminar la distancia.

Devuelve la imagen con el color promedio más cercano al de referencia.
"""
def get_closest_image(avg_color, color_file, image_usage, version):   
    min_distance = float("inf")
    closest_image = None
    with open(color_file, "r") as f:
        for line in f:
            name, r, g, b = line.strip().split(",")
            r, g, b = map(int, (r, g, b))
            distance = 0
            if version == 1:
                # Distancia euclidiana
                distance = math.sqrt((avg_color[0] - r) ** 2 + 
                                     (avg_color[1] - g) ** 2 + 
                                     (avg_color[2] - b) ** 2)
            elif version == 2:
                # Fórmula de distancia de Riemersma
                dr = avg_color[0] - r
                dg = avg_color[1] - g
                db = avg_color[2] - b
                # Ponderación según sensibilidad visual
                distance = math.sqrt(
                    (2 + dr / 256.0) * (dr ** 2) +
                    4 * (dg ** 2) +
                    (2 + (255 - dr) / 256.0) * (db ** 2)
                )
            
            usage_penalty = image_usage.get(name, 0)  # Penalizar imágenes más usadas
            adjusted_distance = distance + usage_penalty * 10  # Ajusta peso según uso
            if adjusted_distance < min_distance:
                min_distance = adjusted_distance
                closest_image = name    
    
    if closest_image:
        image_usage[closest_image] = image_usage.get(closest_image, 0) + 1
    
    return closest_image

"""
Función que procesa una imagen recorriendola por regiones del mismo tamaño.
Por cada región obtiene su color promedio y busca la imagen más cercana en 
color dentro de una biblioteca, esto con el fin de asignarla dentro de la 
región respectiva en una tabla html.

Recibe la imagen a procesar, la ruta al archivo con información de la biblioteca,
el tamaño de las regiones (cuadradas), la ruta de la biblioteca de imágenes para
poder construir la tabla con las referencias adecuadas, y por último, la version 
del tipo de medida que emplea la función que nos devuelve la imagen apropiada para 
cada región.

Devuelve una cadena con el código html para generar un mosaico de imágenes.
"""
def process_image_to_mosaic(img, color_file, region_size, base_library_path, version):    
            
    image = img.convert("RGBA")    
    html = "<html><body><table style='border-collapse: collapse;'>"
    width, height = image.size
    image_usage = {}  # Para rastrear el uso de miniaturas.

    for j in range(0, height, region_size):
        html += "<tr>"
        for i in range(0, width, region_size):
            block_width = min(region_size, width - i)
            block_height = min(region_size, height - j)
            
            # Obtener el color promedio de la región.
            zone_color = get_average_color(image, i, j, block_width, block_height)
            
            # Obtener la miniatura más cercana.
            best_thumbnail_name = get_closest_image(zone_color, color_file, image_usage, version)
            
            # Construir la ruta relativa.
            best_thumbnail_path = os.path.join(base_library_path, best_thumbnail_name)
            best_thumbnail_relative = os.path.relpath(best_thumbnail_path)
            
            # Añadir la celda al HTML.
            html += f"<td style='padding: 0;'>"
            html += f"<img src='{best_thumbnail_relative}' width='{region_size}' height='{region_size}' />"
            html += "</td>"
        
        html += "</tr>"
    
    html += "</table></body></html>"
    
    return html
    



