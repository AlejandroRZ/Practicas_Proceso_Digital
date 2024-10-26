
from PIL import Image
from math import sqrt
"""
Implementación de un procesador de imágenes que aplica filtros básicos.
Archivo que define filtros para añadir una marca de agua.

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
Función que añade una marca de agua a la imagen original.
La marca de agua puede ser añadida en mosaico o en el centro, según el valor de `version`.
version = 1: Añade la marca de agua en mosaico por toda la imagen.
version = 2: Añade una única marca de agua centrada.
"""
def add_image_watermark(original_image, watermark_image, version):

    if original_image:
        background_image = original_image.copy().convert("RGBA")   #Procesamos las imágenes a mezclas
        watermark_image =  watermark_image.convert("RGBA")  
        background_image_width, background_image_height = background_image.size     
        
        watermark = watermark_image.copy()
        r, g, b, alpha = watermark.split()    
        alpha = alpha.point(lambda p: p * 0.3)                      #Generamos canal alfa para la mezcla
        
        watermark = Image.merge("RGBA", (r, g, b, alpha))  

        if version == 1: 
            watermark_width = background_image_width // 5           #Se prepara la miniatura para la marca de agua
            watermark_height = background_image_height // 5            
            watermark.thumbnail((watermark_width, watermark_height), Image.Resampling.LANCZOS)                 

            for i in range(0, background_image_width, watermark_width):        #Imprimimos la marca sobre la imagen en distintas zonas
                for j in range(0, background_image_height, watermark_height):
                    blend_area(watermark, background_image, i, j)
        
        elif version == 2:            
            size_watermark = int(sqrt((background_image_width * background_image_height) // 5)) #Se prepara la miniatura para la marca de agua
            watermark.thumbnail((size_watermark, size_watermark), Image.Resampling.LANCZOS)
            watermark_width, watermark_height = watermark.size
            
            half_width = (background_image_width - watermark_width) // 2  # Calcular las coordenadas para centrar la marca de agua  
            half_height = (background_image_height - watermark_height) // 2            
            blend_area(watermark, background_image, half_width, half_height) # Mezclamos las imágenes en el área central 
        
        return  background_image


""" Función que superpone la marca de agua (upper_image) sobre la imagen de fondo 
(background_image) en las coordenadas (i, j).
"""
def blend_area(upper_image, background_image, i, j):
    watermark_width, watermark_height = upper_image.size  # Tamaño de la marca de agua
    background_image_width, background_image_height = background_image.size   
    box_right = min(i + watermark_width, background_image_width)   # Coordenadas del área en la imagen de fondo
    
    box_bottom = min(j + watermark_height, background_image_height)     
    region_width = box_right - i                    # Tamaño del área a superponer en la imagen de fondo
    region_height = box_bottom - j
    
    upper_image_cropped = upper_image.crop((0, 0, region_width, region_height)) # Recortar la parte de la marca de agua si excede los límites de la imagen de fondo
    mask = upper_image_cropped.split()[3]   # Crear una máscara de transparencia usando el canal alpha de la marca de agua
    background_image.paste(upper_image_cropped, (i, j), mask)  # Superponer la marca de agua sobre la imagen de fondo en la posición (i, j)

