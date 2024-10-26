from PIL import Image, ImageDraw
from .FiltrosColor import grey_scale
from .FiltrosRecursivos import get_average_color, select_best_thumbnail
import random 

"""
Implementación de un procesador de imágenes que aplica filtros por dithering en escala de grises.
Archivo que define filtros por cdithering (Semitonos, azar, ordenado, disperso y Floyd Steinberg).

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 3.7
"""

""" Función que genera una imagen que consta de un ciculo al centro de un 
cuadrado. Se peuden ajustar las dimensiones del círculo y el cuadro,
también se pueden seleccionar los colores para el fondo y el círculo
"""
def generate_dot(diameter, square_length, background_color, dot_color):
    image = Image.new("RGBA", (square_length, square_length), background_color) 
    draw = ImageDraw.Draw(image)
    x0 = (square_length - diameter) // 2
    y0 = (square_length - diameter) // 2     #Generar el fondo y detectar su centro
    x1 = x0 + diameter
    y1 = y0 + diameter
    
    draw.ellipse([x0, y0, x1, y1], fill=dot_color)      #Trazar el círculo
    
    return image

""" Función que recorre una imagen y le aplica un filtro por semitonos. 
Recorre la imagen por sectores de un mismo tamaño y, de acuerdo al color gris
promedio de cada sector, elige la miniatura con un circulo del tamaño adecuado 
para reemplazar dicho sector.
Para lograr lo anterior, previamente convierte la imagen original a escala de grises.
"""
def semitones(original_image, grid_size, background_color, dot_color):
    if original_image:
        grey_image = grey_scale(original_image, 2)         
        result_image = Image.new("RGBA", original_image.size)
        
        
        max_diameter = grid_size 
        num_steps = grid_size         # Crear una lista de imágenes con círculos desde diámetro 0 hasta el máximo
        image_list = []               # posible, el ancho mismo del recuadro     

        for i in range(num_steps + 1):
            diameter = int(i * max_diameter / num_steps)
            dot_image = generate_dot(diameter, grid_size, background_color, dot_color)
            average_dot_grey = get_average_color(dot_image, 0, 0, dot_image.width, dot_image.height, 1)
            dot_grey = (average_dot_grey, average_dot_grey, average_dot_grey)            
            image_list.append((dot_grey, dot_image)) 
            if diameter == max_diameter:
                break;     
        
        for i in range(0, original_image.width, grid_size):                    
            for j in range(0, original_image.height, grid_size):       #Generar el mosaico             
                block_width = min(grid_size, original_image.width - i)
                block_height = min(grid_size, original_image.height - j)                                         
                zone_grey = get_average_color(grey_image, i, j, block_width, block_height, 1) 
                zone_color = (zone_grey, zone_grey, zone_grey,  255)          
                best_thumbnail = select_best_thumbnail(image_list, zone_color, 2)                    
                result_image.paste(best_thumbnail, (i, j))  

        return result_image

""" Función que aplica dithering al azar. Recorre la imagen pixel por pixel
y según un umbral elegido al azar, si el valor del gris original es mayor pone el
pixel en blanco, si es menor lo pone en negro.
Previamente se convierte la imagen original a escala de grises.
"""
def random_dithering(reference_image): 
    image_width, image_height = reference_image.size
    result_image = Image.new("RGBA", reference_image.size) 
    result_pixels = result_image.load() 
    reference_pixels = reference_image.load()

    for x in range(image_width):
        for y in range(image_height):
            r, g, b, a = reference_pixels[x, y]
            random_threshold = random.randint(0, 255)  # Genera un valor aleatorio para el umbral
            new_pixel = 255 if r > random_threshold else 0
            result_pixels[x, y] = (new_pixel, new_pixel, new_pixel, a)
    
    return result_image

""" Función que aplica dithering por matriz. Recorre la imagen pixel por pixel
y toma el valor del gris en turno escalado de 0-9, si dicho valor es menor que
el valor que le corresponde en la matriz de referencia, se pone el pixel en 
en negro, si es mayor se pone en blanco.
Previamente se convierte la imagen original a escala de grises, además, el recorrido pixel
por pixel según lo estipulado, emula un recorrido por regiones de 3x3.
Hay 2 matrices posibles por el momento, ordenada y dispersa.
"""
def matrix_dithering(reference_image, matrix):
    image_width, image_height = reference_image.size
    result_image = Image.new("RGBA", reference_image.size) 
    result_pixels = result_image.load()
    reference_pixels = reference_image.load()    
    matrix_size = len(matrix)

    for x in range(image_width):
        for y in range(image_height):
            r, g, b, a = reference_pixels[x, y]
            scaled_pixel_value = r // 28 
            matrix_value = matrix[y % matrix_size][x % matrix_size]  # Obtener el valor de la matriz en la posición correspondiente           
            
            if scaled_pixel_value < matrix_value:
                result_pixels[x, y] = (0, 0, 0, a)  # Negro
            else:
                result_pixels[x, y] = (255, 255, 255, a)  # Blanco
    
    return result_image
    
    
"""Función que aplica el algoritmo de dithering de Floyd-Steinberg a una imagen en escala de grises.
Recorre cada píxel, ajustando su valor a blanco o negro y distribuyendo el error de cuantización
a los píxeles vecinos según el método de Floyd-Steinberg.
"""
def floyd_steinberg_dithering(reference_image):    
    image_width, image_height = reference_image.size
    result_image = Image.new("RGBA", reference_image.size) #Preparación de la imagen
    reference_pixels = reference_image.load()  
    result_pixels = result_image.load()
    
    for x in range(image_width):
        for y in range(image_height):
            old_pixel, g, b, a = reference_pixels[x, y] #Determinar el color del pixel
            new_pixel = 255 if old_pixel > 127 else 0  
            result_pixels[x, y] = (new_pixel, new_pixel, new_pixel, a)
            
            # Calcular el error de cuantización
            quant_error = old_pixel - new_pixel
            
            # Distribuir el error a los píxeles vecinos, si existen
            if y + 1 < image_height:  # Abajo
                r, g, b, a = reference_pixels[x, y + 1]
                error_color = int(min(max(r + quant_error * 7 / 16, 0), 255))
                reference_pixels[x, y + 1] = (error_color, error_color, error_color, a)
            
            if x + 1 < image_width and y - 1 >= 0:  # Derecha arriba
                r, g, b, a = reference_pixels[x + 1, y - 1]
                error_color = int(min(max(r + quant_error * 3 / 16, 0), 255))
                reference_pixels[x + 1, y - 1] = (error_color, error_color, error_color, a)
            
            if x + 1 < image_width:  # Derecha                
                r, g, b, a = reference_pixels[x + 1, y]
                error_color = int(min(max(r + quant_error * 5 / 16, 0), 255))
                reference_pixels[x + 1, y] = (error_color, error_color, error_color, a)
            
            if x + 1 < image_width and y + 1 < image_height:  # Derecha abajo
                r, g, b, a = reference_pixels[x + 1, y + 1]
                error_color = int(min(max(r + quant_error * 1 / 16, 0), 255))
                reference_pixels[x + 1, y + 1] = (error_color, error_color, error_color, a)
    
    return result_image
    
    
"""Función que selecciona el tipo de dithering a aplicar basado en una versión específica.
Convierte la imagen original a escala de grises antes de aplicar el algoritmo de dithering
correspondiente (aleatorio, con matriz dispersa o agrupada, o Floyd-Steinberg).
"""
def dithering(original_image, version):
    if original_image:
        grey_image = grey_scale(original_image, 2) 
        result_image = None
        if version == 1 :
            result_image = random_dithering(grey_image)
        elif version == 2 :
            clustered_matrix = [
                [8, 3, 4],  
                [6, 1, 2],
                [7, 5, 9] 
            ]
            result_image = matrix_dithering(grey_image, clustered_matrix)
        elif version == 3 :
            dispersed_matrix = [
                [1, 7, 4],  
                [5, 8, 3],
                [6, 2, 9] 
            ]
            result_image = matrix_dithering(grey_image, dispersed_matrix)
        elif version == 4 :
            result_image = floyd_steinberg_dithering(grey_image)

        return result_image