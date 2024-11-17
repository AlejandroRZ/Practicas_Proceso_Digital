from PIL import Image, ImageDraw, ImageFont
from Filtros import FiltrosColor
from .FiltrosRecursivos import get_average_color
"""
Implementación de un procesador de imágenes que aplica filtros básicos.
Archivo en el que se definene funciones para filtros artisticos.

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 3.7
"""
    
""" 
Función que aplica el filtro acuarela (conocido también como óleo).
Este filtro recorre la imágen pixel a pixel y visita una vecindad cuadrada del mismo
cuyo tamaño podemos definir, obtiene un histograma de los colores y asigna al pixel el color 
más repetido o en su defecto, el color promedio de la vecindad.
"""  
def watercolor(original_image, matrix_size, version):
    if original_image and (version ==1 or version == 2):
        original_image =  original_image.copy().convert("RGBA")   
        watercolor_image = Image.new("RGBA", original_image.size) 
        watercolor_pixels = watercolor_image.load()

        if version == 2:
            original_image = FiltrosColor.grey_scale(original_image, 2)
        
        original_pixels = original_image.load()

        image_width, image_height = original_image.size
        radius = matrix_size // 2

        # Recorrer todos los píxeles de la imagen
        for x in range(image_width):
            for y in range(image_height):
                # Crear una lista para almacenar los colores de la vecindad
                color_count = {}                 
                # Recorrer la vecindad alrededor del píxel (x, y)
                for i in range(matrix_size):
                    for j in range(matrix_size):
                        offset_x = i - radius
                        offset_y = j - radius
                        nx = x + offset_x
                        ny = y + offset_y

                        if 0 <= nx < image_width and 0 <= ny < image_height:
                            current_color = original_pixels[nx, ny]
                                
                            # Si el color ya está en el diccionario, incrementar el contador
                            if current_color in color_count:
                                color_count[current_color] += 1
                            else:
                                color_count[current_color] = 1

                # Encontrar el color más común
                most_common_color = max(color_count, key=color_count.get)
                
                # Si no hay un color que se repita más, calcular el promedio
                if color_count[most_common_color] == 1:
                    avg_r = sum([color[0] for color in color_count.keys()]) // len(color_count)
                    avg_g = sum([color[1] for color in color_count.keys()]) // len(color_count)
                    avg_b = sum([color[2] for color in color_count.keys()]) // len(color_count)
                    avg_a = sum([color[3] for color in color_count.keys()]) // len(color_count)
                    watercolor_pixels[x, y] = (avg_r, avg_g, avg_b, avg_a)
                else:
                    watercolor_pixels[x, y] = most_common_color

        return watercolor_image
    

def letters_filter(original_image, section_width, section_height, version):
    if original_image:
        original_image =  original_image.copy().convert("RGBA")
        if version == 1:
            original_image = FiltrosColor.grey_scale(original_image, 2)
        width, height = original_image.size
        html = "<!DOCTYPE html>\n<html>\n<head>\n<style>\n"
        html += "body { font-family: monospace; line-height: 1; }\n</style>\n</head>\n<body>\n<pre>\n"

        # Create a blank new image
        new_image = Image.new("RGBA", (width, height), (255,255,255,0))
        draw = ImageDraw.Draw(new_image)
        
        # Use a font for the letters (adjust the path based on your system if needed)
        try:
            font = ImageFont.truetype("arial.ttf", section_height)
        except IOError:
            font = ImageFont.load_default()

        for y in range(0, height, section_height):
            for x in range(0, width, section_width):   #r, g y b iguales si la versión es 1
                r, g, b, a = get_average_color(original_image, x, y, section_width, section_height, version)               
                
                html += f'<span style="color: rgba({r},{g},{b},{a/255});">M</span>'                
                draw.text((x, y), "M", fill=(r,g,b,a), font=font)

            html += "\n"  

        html += "</pre>\n</body>\n</html>"
        return html, new_image

