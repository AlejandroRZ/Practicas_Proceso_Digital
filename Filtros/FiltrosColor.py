from PIL import Image
"""
Implementación de un procesador de imágenes que aplica filtros básicos.
Archivo en el que se definene funciones para filtros básicos de color.

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 3.7
"""

""" Función que implementa 2 filtros de escala de grises.
El primero de ellos emplea una media simple y el segundo una media ponderada.
"""
def grey_scale(original_image, version):
    if original_image:   
        original_image =  original_image.copy().convert("RGBA")   
        grey_img = Image.new("RGBA", original_image.size) # Crear una nueva imagen en modo RGB para almacenar el resultado del filtro
        
        pixels = original_image.load()
        grey_pixels = grey_img.load()

        # Recorre la imagen pixel a pixel y les aplica la formula de la media ó de la media
        # ponderada para convertir a escala de grises.        
        for i in range(original_image.width):
            for j in range(original_image.height):
                r, g, b, a = pixels[i, j]
                grey = (r + g + b) // 3

                if version == 2:
                    grey = int(r*0.299 + g*0.587 + b*0.114)

                grey_pixels[i, j] = (grey, grey, grey, a)
         
        return grey_img
    

""" Función que aplica el filtro de mica, es decir, cambia la paleta de colores 
    de la imagen por una que toma como base a un sólo color RGB.
"""
def rgb_glass(original_image, version):
    if original_image:
        original_image =  original_image.copy().convert("RGBA")   
        glass_image = Image.new("RGBA", original_image.size)      
        pixels = original_image.load()
        rgb_pixels = glass_image.load()

        # Recorre la imagen pixel a pixel y mantiene únicamente un valor de los bytes RGB
        # los 2 restantes los establece en cero.  
        for i in range(original_image.width):
            for j in range(original_image.height):
                r, g, b, a = pixels[i, j]

                if version == 1:
                    rgb_pixels[i, j] = (r, 0, 0, a)
                elif version == 2:
                    rgb_pixels[i, j] = (0, g, 0, a)
                else:
                    rgb_pixels[i, j] = (0, 0, b, a)

        return glass_image
    
""" Función que mezcla los colores de una imágen con
otro color de referencia, para tener una paleta afin a este último.
"""
def color_filter(image, color):    
    rgb_image = image.copy().convert('RGBA')  
    width, height = rgb_image.size    
    filter_r, filter_g, filter_b = color                # Preparamos la imagen a procesar
    filtered_image = Image.new('RGBA', (width, height))  # así como el color de referencia
    original_pixels = rgb_image.load()
    filtered_pixels = filtered_image.load()    
    
    for i in range(width):
        for j in range(height):            
            original_r, original_g, original_b, original_a = original_pixels[i, j]  # Mezclamos colores
            new_r = (original_r + filter_r) // 2
            new_g = (original_g + filter_g) // 2
            new_b = (original_b + filter_b) // 2          
            filtered_pixels[i, j] = (new_r, new_g, new_b, original_a)
    
    return filtered_image     