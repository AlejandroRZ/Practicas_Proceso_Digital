from tkinter import filedialog
from PIL import Image
import os 

def recursive_image_generation(version, reference_image):
    if reference_image:
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona la imagen para el mosaico", filetypes=(("JPG file","*.jpg"), ("PNG file", "*.png")))
        if filename:
            
            #Imagen para rellenar y  la imagen que rellenaremos
            filler_image = Image.open(filename) 
            recursive_image = Image.new("RGB", reference_image.size)

            # Obtener los datos de píxeles de la imagen original y los de la que rellenaremos
            original_pixels = reference_image.load()
            recursive_pixels = recursive_image.load()
            filler_pixels = filler_image.load()
            image_list = []
            tile_width = 10
            tile_height = 10

            if version == 1:
                
                for i in range(reference_image.width):
                    for j in range(reference_image.height):
                        r, g, b = original_pixels[i, j]                            
                        grey = int(r*0.299 + g*0.587 + b*0.114)                        
                        recursive_pixels[i, j] = (grey, grey, grey) 
                    #Hasta aquí, se generó una copia en gris de la orginal
               
                for i in range(filler_image.width):
                    for j in range(filler_image.height):
                        r_fill, g_fill, b_fill = filler_pixels[i, j]
                        grey_fill = int(r_fill*0.299 + g_fill*0.587 + b_fill*0.114) #Aquí el filler se pasó a gris
                        filler_pixels[i, j] = (grey_fill, grey_fill, grey_fill)         

                for i in range (30): 
                    factor = ((i + 1.0) / 15.0) ** 2
                    temp_img = filler_image.copy().resize((tile_width, tile_height))
                    temp_pixels = temp_img.load()                    
                    brightness_mod(temp_img, temp_pixels, factor)                   
                    image_list.append(temp_img) 
                     # Definir el tamaño de las celdas del mosaico (por ejemplo, 10x10 píxeles)             
              
                for i in range(0, recursive_image.width, tile_width):                    
                    for j in range(0, recursive_image.height, tile_height):
                        block_width = min(tile_width, recursive_image.width - i)
                        block_height = min(tile_height, recursive_image.height - j)                        
                        zone_grey = get_average_grey(recursive_image, i, j, block_width, block_height)                       
                        best_thumbnail = select_best_thumbnail(image_list, zone_grey)
                        recursive_image.paste(best_thumbnail, (i, j))

            elif version == 2:  
                
                



        return recursive_image
                                      

           

def brightness_mod(temp_img, bright_pixels, factor):
         
    for i in range(temp_img.width):
        for j in range(temp_img.height):
            r, g, b = bright_pixels[i, j]
            new_r = min(max(int(r * factor), 0), 255)
            new_g = min(max(int(g * factor), 0), 255)
            new_b = min(max(int(b * factor), 0), 255)
            bright_pixels[i, j] = (new_r, new_g, new_b)


def get_average_grey(image, x, y, width, height): 
    
    # Calcular el promedio de los valores de gris en una región
    pixels = image.load()
    total_grey = 0
    count = 0
    for i in range(x, min(x + width, image.width)):
        for j in range(y, min(y + height, image.height)):
            grey = pixels[i, j][0] # Tomar el valor de gris (R=G=B)
            total_grey += grey
            count += 1
            print(f'count {count}')
    return total_grey // count if count > 0 else 0

# aquí hay algún problema, me devuelve nones

def select_best_thumbnail(image_list, target_grey):
    # El tamaño del intervalo es aproximadamente 8.5
    interval_size = 255 / 30
    
    # Calcula el índice correspondiente
    index = int(target_grey / interval_size)
       
    return image_list[index]
             



     

                  
def exportar_imagenes(image_list):
    ruta_destino = "/home/alejandrorz/Documentos"
    for i, img in enumerate(image_list):
        # Genera un nombre de archivo único para cada imagen
        filename = f"imagen_{i+1}.png"
        filepath = os.path.join(ruta_destino, filename)
        
        # Guarda la imagen en el directorio especificado
        img.save(filepath)
        print(f"Imagen guardada en: {filepath}")



