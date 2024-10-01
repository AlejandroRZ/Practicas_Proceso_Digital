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

Versión 2.0
"""

""" Función que implementa 2 filtros de escala de grises.
El primero de ellos emplea una media simple y el segundo una media ponderada"""

def grey_scale(original_image, version):
    if original_image:        
        grey_img = Image.new("RGB", original_image.size) # Crear una nueva imagen en modo RGB para almacenar el resultado del filtro
        pixels = original_image.load()
        grey_pixels = grey_img.load()

        # Recorre la imagen pixel a pixel y les aplica la formula de la media ó de la media
        # ponderada para convertir a escala de grises.        
        for i in range(original_image.width):
            for j in range(original_image.height):
                r, g, b = pixels[i, j]
                grey = (r + g + b) // 3

                if version == 2:
                    grey = int(r*0.299 + g*0.587 + b*0.114)

                grey_pixels[i, j] = (grey, grey, grey)
         
        return grey_img
    

""" Función que aplica el filtro de mica, es decir, cambia la paleta de colores 
    de la imagen por una que toma como base a un sólo color RGB."""

def rgb_glass(original_image, version):
    if original_image:
        
        glass_image = Image.new("RGB", original_image.size)      
        pixels = original_image.load()
        rgb_pixels = glass_image.load()

        # Recorre la imagen pixel a pixel y mantiene únicamente un valor de los bytes RGB
        # los 2 restantes los establece en cero.  
        for i in range(original_image.width):
            for j in range(original_image.height):
                r, g, b = pixels[i, j]

                if version == 1:
                    rgb_pixels[i, j] = (r, 0, 0)
                elif version == 2:
                    rgb_pixels[i, j] = (0, g, 0)
                else:
                    rgb_pixels[i, j] = (0, 0, b)

        return glass_image
