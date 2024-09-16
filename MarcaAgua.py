
from PIL import Image
from math import sqrt

def add_image_watermark(original_image, version):

    if original_image:
        background_image = original_image.copy().convert("RGBA") 
        background_image_width, background_image_height = background_image.size        
        watermark_image = Image.open("walruss.png").convert("RGBA")
        watermark = watermark_image.copy()
        r, g, b, alpha = watermark.split()    
        alpha = alpha.point(lambda p: p * 0.3)
        watermark = Image.merge("RGBA", (r, g, b, alpha))  

        if version == 1: 
            watermark_width = background_image_width // 5
            watermark_height = background_image_height // 5            
            watermark.thumbnail((watermark_width, watermark_height), Image.Resampling.LANCZOS)                 

            for i in range(0, background_image_width, watermark_width):
                for j in range(0, background_image_height, watermark_height):
                    blend_area(watermark, background_image, i, j)
        
        elif version == 2:            
            size_watermark = int(sqrt((background_image_width * background_image_height) // 5))
            watermark.thumbnail((size_watermark, size_watermark), Image.Resampling.LANCZOS)
            watermark_width, watermark_height = watermark.size
            
            # Calcular las coordenadas para centrar la marca de agua
            half_width = (background_image_width - watermark_width) // 2
            half_height = (background_image_height - watermark_height) // 2
            
            blend_area(watermark, background_image, half_width, half_height)
        
        return  background_image



def blend_area(upper_image, background_image, i, j):
     # Tamaño de la marca de agua
    watermark_width, watermark_height = upper_image.size
    background_image_width, background_image_height = background_image.size

    # Coordenadas del área en la imagen de fondo
    box_right = min(i + watermark_width, background_image_width)
    box_bottom = min(j + watermark_height, background_image_height)
    
    # Tamaño del área a superponer en la imagen de fondo
    region_width = box_right - i
    region_height = box_bottom - j
    
    # Recortar la parte de la marca de agua si excede los límites de la imagen de fondo
    upper_image_cropped = upper_image.crop((0, 0, region_width, region_height))
    
    # Crear una máscara de transparencia usando el canal alpha de la marca de agua
    mask = upper_image_cropped.split()[3]  # Canal alpha
    
    # Superponer la marca de agua sobre la imagen de fondo en la posición (i, j)
    background_image.paste(upper_image_cropped, (i, j), mask)

