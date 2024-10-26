from PIL import Image
from Filtros import FiltrosColor

"""
Implementación de un procesador de imágenes que aplica filtros básicos.
Archivo en el que se definene funciones para filtros variados.

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 3.7
"""

""" Función que aplica el filtro de erosión sobre una imagen de entrada.
Recorre la imagen pixel a pixel y visita la vecindad de cada uno en un radio
definido. Dentro de tal radio elige el color más brillante o el menos brillante
y lo asigna al pixel en turno. Cuando se elige al color más brillante tenemos
una erosión por máximos, en caso contrario, tenemos una erosión por minímos.
Usamos una imagen clon en escala de grises como guia para determinar el brillo.
"""
def erosion(original_image, matrix_size, version):
    if original_image and (version == 1 or version == 2):
        original_image =  original_image.copy().convert("RGBA")   
        eroded_image = Image.new("RGBA", original_image.size)  #Preparamos las imágenes
        backup_image = FiltrosColor.grey_scale(original_image, 2)  #Imagen en escala de grises para la referencia   
        original_pixels = original_image.load()
        eroded_pixels = eroded_image.load()
        backup_pixels = backup_image.load()

        image_width, image_height = original_image.size
        radius = matrix_size // 2

        #Recorrido de la imagen pixel a pixel
        for x in range(image_width):
            for y in range(image_height):
                right_position = (x, y)
                right_color = original_pixels[x, y]

                for i in range(radius):
                    for j in range(radius):
                        offset_x = i - radius
                        offset_y = j - radius   #Recorremos una vecindad definida
                        nx = x + offset_x
                        ny = y + offset_y                        

                        if 0 <= nx < image_width and 0 <= ny < image_height:                            
                            reference_grey = backup_pixels[nx, ny][0]        #Tomamos sólo pixeles dentro de lrango permitido

                            if (version == 1 and reference_grey > right_color[0]) or  (version == 2 and reference_grey < right_color[0]):
                                right_position = (nx, ny)       #Elegimos el máximo o el mínimo
                                

                eroded_pixels[x, y] =  original_pixels[right_position] 
        
        return eroded_image 
                            