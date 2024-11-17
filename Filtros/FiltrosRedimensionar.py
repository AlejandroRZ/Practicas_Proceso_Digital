from PIL import Image
"""
Implementación de un procesador de imágenes que aplica filtros básicos.
Archivo en el que se definene funciones para filtros de redimensión.
Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 4.0
"""

""" Función cúbica auxiliar para el algoritmo de interpolación bicúbica.
Esta función calcula el peso cúbico para un píxel basado en la distancia entre 
el píxel original y la posición fraccionaria en la imagen. Utiliza una función cúbica
que asegura suavidad en las transiciones, ajustada por el parámetro 'a' 
(que por defecto es -0.5, correspondiente a la interpolación bicúbica estándar).
"""
def cubic(x, a=-0.5):
    abs_x = abs(x)
    if abs_x <= 1:
        return (a + 2) * (abs_x ** 3) - (a + 3) * (abs_x ** 2) + 1
    elif 1 < abs_x < 2:
        return a * (abs_x ** 3) - 5 * a * (abs_x ** 2) + 8 * a * abs_x - 4 * a
    return 0


""" Función para la interpolación bicúbica de un píxel en una posición fraccionaria.
Esta función calcula el color interpolado de un píxel en una posición fraccionaria 
(x, y) dentro de la imagen original. Utiliza los 16 píxeles vecinos más cercanos 
(dentro de una cuadrícula 4x4) para estimar el valor del color mediante 
la combinación ponderada de los valores de los píxeles vecinos.
"""
def bicubic_interpolation(original_pixels, x, y, width, height):
    x0 = int(x)
    y0 = int(y)    
    interpolated_value = [0, 0, 0, 0]  # RGBA

    for i in range(-1, 3):
        for j in range(-1, 3):
            neighbor_x = min(max(x0 + i, 0), width - 1)
            neighbor_y = min(max(y0 + j, 0), height - 1)
            pixel_value = original_pixels[neighbor_x, neighbor_y]

            # Calcular el peso cúbico en x y en y
            weight_x = cubic(x - neighbor_x)
            weight_y = cubic(y - neighbor_y)

            # Acumular el valor interpolado
            for k in range(4):  # RGBA
                interpolated_value[k] += pixel_value[k] * weight_x * weight_y

    # Asegurar que los valores de cada canal estén en el rango 0-255
    return tuple(min(max(int(v), 0), 255) for v in interpolated_value)


""" Función que aplica filtros de redimensionado, recibe la imagen a
escalar y el porcentaje de escala. Si el valor recibido se encuentra
entre 0 y 1 (intervalo abierto) entonces aplica la formúla para escalar hacia abajo
que consta de tomar cada pixel (x,y) y redirigirlo a la posición (piso_entero(scale*x), piso_entero(scale*y)).
Si el valor de la escala es superior a 1, se aplica el algoritmo de interpolación bicúbica.
"""
def resize_image(original_image, scale):
    if original_image:   

        original_image =  original_image.copy().convert("RGBA") 
        width, height = original_image.size
        original_pixels = original_image.load()
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_image = Image.new("RGBA", (new_width, new_height))
        resized_pixels = resized_image.load() 

        if scale < 1:
            #Escala hacia abajo    
            for i in range(width):
                for j in range(height):                                                           
                    new_i = int(i * scale)
                    new_j = int(j * scale)
                    resized_pixels[new_i, new_j] = original_pixels[i, j]
        else:   
            #Escala hacia arriba    
            for new_i in range(new_width):
                for new_j in range(new_height):
                    # Coordenadas fraccionarias en la imagen original
                    original_i = new_i / scale
                    original_j = new_j / scale

                    # Calcular el color del píxel usando interpolación bicúbica
                    resized_pixels[new_i, new_j] = bicubic_interpolation(original_pixels, original_i, original_j, width, height)                
            
        return resized_image
    

