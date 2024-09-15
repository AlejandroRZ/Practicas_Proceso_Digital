from PIL import Image

""" Función que define el recorrido de una imagen pixel por pixel y aplica
    la convolución dada una matriz pertinente, además de un factor y un cesgo 
    que permiten mantener el brillo base."""

def convolution_core(original_image, matrix_filtr, factor, bias):
    if original_image:
        convol_img = Image.new("RGB", original_image.size)        
        pixels = original_image.load()
        convol_pixels = convol_img.load()
        matrix_height = len(matrix_filtr)
        matrix_width = len(matrix_filtr[0])       
        

        for img_column in range(original_image.width):
            for img_row in range(original_image.height):

                sum_r, sum_g, sum_b = 0, 0, 0  
                
                for matrix_row in range(matrix_height):
                    for matrix_column in range(matrix_width):                        

                        # Calcular la posición del píxel en la imagen
                        prod_column = (img_column - (matrix_width // 2) + matrix_column) % original_image.width
                        prod_row = (img_row - (matrix_height // 2) + matrix_row) % original_image.height
                        
                        # Obtener el valor del píxel correspondiente
                        r, g, b = pixels[prod_column, prod_row]

                        # Aplicar el filtro (convolución)
                        sum_r += r * matrix_filtr[matrix_row][matrix_column]
                        sum_g += g * matrix_filtr[matrix_row][matrix_column]
                        sum_b += b * matrix_filtr[matrix_row][matrix_column]

                # Asegurarse de que los valores de los píxeles estén en el rango correcto [0, 255]
                sum_r = min(max(int(factor*sum_r + bias), 0), 255)
                sum_g = min(max(int(factor*sum_g + bias), 0), 255)
                sum_b = min(max(int(factor*sum_b + bias), 0), 255)

                # Asignar el nuevo valor al píxel convolutionado
                convol_pixels[img_column, img_row] = (sum_r, sum_g, sum_b)         

        return convol_img 

# Auxiliares para llamar a cada filtro en su respectivo submenú.
def convolution(original_image, version):
    
    if version == 1:        
        blur_matrix = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0]
        ] 
        factor = 1.0 / 41.0
        bias =  0.0 
        return convolution_core(original_image, blur_matrix, factor, bias)

    elif version == 2:
        mblur_matrix= [
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1]
        ]
        factor = 1.0 / 9.0
        bias = 0.0
        return convolution_core(original_image, mblur_matrix, factor, bias)
    
    elif version == 3:
        bsharp_matrix = [
            [-1, -1, -1, -1, -1],
            [-1,  2,  2,  2, -1],
            [-1,  2,  8,  2, -1],
            [-1,  2,  2,  2, -1],
            [-1, -1, -1, -1, -1],
        ]
        factor = 1.0 / 8.0
        bias = 0.0
        return convolution_core(original_image, bsharp_matrix, factor, bias)

    elif version == 4:
        bfind_matrix = [
            [0,  0, -1,  0,  0],
            [0,  0, -1,  0,  0],
            [0,  0,  2,  0,  0],
            [0,  0,  0,  0,  0],
            [0,  0,  0,  0,  0]
        ]
        factor = 1.0
        bias = 0.0
        return convolution_core(original_image, bfind_matrix, factor, bias)
    
    elif version == 5:
        emb_matrix = [
            [-1, -1,  0],
            [-1,  0,  1],
            [0,  1,  1]
        ]
        factor = 1.0
        bias = 128.0
        return convolution_core(original_image, emb_matrix, factor, bias)

    elif version == 6:
        mean_matrix = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ] 
        factor = 1.0 / 25.0;
        bias = 0.0;
        return convolution_core(original_image, mean_matrix, factor, bias)    


   
