from PIL import Image
from .FiltrosColor import grey_scale, color_filter
import csv, ast, math 
import importlib.resources as pkg_resources


"""
Implementación de un procesador de imágenes que aplica filtros básicos.
Archivo que define 2 filtros que generan mosaicos de una imagen empleando otras imágenes.

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 3.5
"""

""" Función que genera una imagen de forma recursiva a partir de una imagen de referencia 
y una imagen de relleno (filler).
Dependiendo de la `version`, el algoritmo funciona en escala de grises (version 1) o con 
colores de una paleta (version 2). 
"""
def recursive_image_generation(reference_image, filler_image, version, tile_width, tile_height):    
    if reference_image and filler_image:
        reference_image = reference_image.copy().convert('RGBA') 
        filler_image = filler_image.copy().convert('RGBA')   
        recursive_image = Image.new("RGBA", reference_image.size)            
        image_list = []
        
        if version == 1: 
            recursive_image = grey_scale(reference_image.copy(), 2)  #Pasamos a escala de grises a la
            filler_image =  grey_scale(filler_image, 2)              #imagen base y a la de relleno   

            for i in range (30):                       # Se ajusta el brillo de las miniaturas
                factor = ((i + 1.0) / 15.0) ** 2       # Para tener una gama de tonos        
                temp_img = filler_image.copy().resize((tile_width, tile_height), Image.Resampling.LANCZOS)
                temp_pixels = temp_img.load() 
                brightness_mod(temp_img, temp_pixels, factor)                   
                image_list.append(temp_img) 
        
        elif version == 2:                 
            webpalette_rgb_codes = []    
            with pkg_resources.open_text('Filtros.data', 'WebPalette.csv') as csv_file_palette:
                reader = csv.DictReader(csv_file_palette)    
                                                        #Recoger el listado de colores de la Web palette
                for row in reader:                       
                    triplet = ast.literal_eval(row['rgb_values'])
                    webpalette_rgb_codes.append(triplet)            
                                                        # Aplicar el filtro de color a la imagen y guardar las copias
            for i, color in enumerate(webpalette_rgb_codes):
                filtered_image = color_filter(filler_image.copy().resize((tile_width, tile_height), Image.Resampling.LANCZOS), color)             
                image_list.append((color, filtered_image))
                
        for i in range(0, recursive_image.width, tile_width):                    
            for j in range(0, recursive_image.height, tile_height):       #Generar el mosaico             
                block_width = min(tile_width, recursive_image.width - i)
                block_height = min(tile_height, recursive_image.height - j)                                         
                zone_color = get_average_color(reference_image, i, j, block_width, block_height, version)           
                best_thumbnail = select_best_thumbnail(image_list, zone_color, version)                    
                recursive_image.paste(best_thumbnail, (i, j))     

    return recursive_image
                                      
           
"""Funcion que ajusta el brillo de los pixeles de acuerdo a un factor dado."""

def brightness_mod(temp_img, bright_pixels, factor):         
    for i in range(temp_img.width):
        for j in range(temp_img.height):
            r, g, b, a = bright_pixels[i, j]
            new_r = min(max(int(r * factor), 0), 255)
            new_g = min(max(int(g * factor), 0), 255)
            new_b = min(max(int(b * factor), 0), 255)
            bright_pixels[i, j] = (new_r, new_g, new_b, a)

"""Función para obtener el color promedio de una zona dentro de una imagen"""

def get_average_color(image, x, y, width, height, version):  
    pixels = image.load()
    total_r, total_g, total_b, count, a = 0, 0, 0, 0, 0    
    average_color = -1

    if version == 1 or version == 2:
        for i in range(x, min(x + width, image.width)):
            for j in range(y, min(y + height, image.height)):

                if version == 1:
                    grey = pixels[i, j][0] # Tomar el valor de gris (R=G=B)
                    total_g += grey
                else:
                    temp_r, temp_g, temp_b, a = pixels[i, j]
                    total_r += temp_r                       # Genera la suma para el promedio
                    total_g += temp_g
                    total_b += temp_b

                count += 1

        if count == 0:
            average_color = 0
        elif version == 1:
            average_color = total_g // count
        else:
            average_color = (total_r // count, total_g // count, total_b // count, a)
    
    return average_color


""" Función que nos permite elegir la miniatura más adecuada para reemplazar una zona
de la imagen de referencia con base en su color promedio. 
"""
def select_best_thumbnail(image_list, target_color, version):
    right_index = 0
    minimum_difference = float('inf')

    if version == 1:     
        interval_size = 255 / 30        
        right_index = max(0, min(int(target_color / interval_size), 29))  #  Empleamos indexación para elegir el tono de
        best_thumbnail = image_list[right_index]         # gris promedio más idóneo   

    elif version == 2:        
        for ind, couple in enumerate(image_list):
            temp_r, temp_g, temp_b = couple[0]            # Se elige el tono cuya diferencia sea la menor
            target_r, target_g, target_b, target_a = target_color   # respecto del color promedio de la zona                    
            temp_difference = math.sqrt((temp_r - target_r)**2 + (temp_g - target_g)**2 + (temp_b - target_b)**2 )

            if temp_difference < minimum_difference:                
                minimum_difference = temp_difference
                right_index = ind 

        best_thumbnail_tuple = image_list[right_index]
        best_thumbnail = best_thumbnail_tuple[1] 

    return best_thumbnail




                  

