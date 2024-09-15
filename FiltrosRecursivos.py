from tkinter import filedialog
from PIL import Image
import os, csv, ast, math 


def recursive_image_generation(version, reference_image):
    
    if reference_image:        
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona la imagen para el mosaico", filetypes=(("JPG file","*.jpg"), ("PNG file", "*.png")))
        
        if filename: 
            filler_image = Image.open(filename)
            recursive_image = Image.new("RGB", reference_image.size)            
            image_list = []
            tile_width = 15
            tile_height = 15

            if version == 1:                
                original_pixels = reference_image.load()
                recursive_pixels = recursive_image.load()
                filler_pixels = filler_image.load()

                for i in range(reference_image.width):
                    for j in range(reference_image.height):
                        r, g, b = original_pixels[i, j]                            
                        grey = int(r*0.299 + g*0.587 + b*0.114)                        
                        recursive_pixels[i, j] = (grey, grey, grey)                
               
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
                    image_list.append(temp_img)                    # Definir el tamaño de las celdas del mosaico (por ejemplo, 10x10 píxeles)             
           
            elif version == 2:                 
                webpalette_rgb_codes = []
                recursive_image = reference_image                
                
                with open('WebPalette.csv', mode='r') as csv_file_palette:
                    reader = csv.DictReader(csv_file_palette)    
                    
                    for row in reader:                       
                        triplet = ast.literal_eval(row['rgb_values'])
                        webpalette_rgb_codes.append(triplet)
                
                # Aplicar el filtro de color a la imagen y guardar las copias
                for i, color in enumerate(webpalette_rgb_codes):
                    filtered_image = color_filter(filler_image.copy().resize((tile_width, tile_height)), color)
                    image_list.append((color, filtered_image))
                   
            for i in range(0, recursive_image.width, tile_width):                    
                for j in range(0, recursive_image.height, tile_height):                    
                    block_width = min(tile_width, recursive_image.width - i)
                    block_height = min(tile_height, recursive_image.height - j)                                         
                    zone_color = get_average_color(recursive_image, i, j, block_width, block_height, version)
                    best_thumbnail = select_best_thumbnail(image_list, zone_color, version)                    
                    recursive_image.paste(best_thumbnail, (i, j))     

        return recursive_image
                                      

           

def brightness_mod(temp_img, bright_pixels, factor):
         
    for i in range(temp_img.width):
        for j in range(temp_img.height):
            r, g, b = bright_pixels[i, j]
            new_r = min(max(int(r * factor), 0), 255)
            new_g = min(max(int(g * factor), 0), 255)
            new_b = min(max(int(b * factor), 0), 255)
            bright_pixels[i, j] = (new_r, new_g, new_b)


def get_average_color(image, x, y, width, height, version):  
    pixels = image.load()
    total_r = 0
    total_g = 0
    total_b = 0
    count = 0
    average_color = -1

    if version == 1 or version == 2:

        for i in range(x, min(x + width, image.width)):
            for j in range(y, min(y + height, image.height)):

                if version == 1:
                    grey = pixels[i, j][0] # Tomar el valor de gris (R=G=B)
                    total_g += grey
                else:
                    temp_r, temp_g, temp_b = pixels[i, j]
                    total_r += temp_r
                    total_g += temp_g
                    total_b += temp_b
                count += 1

        if count == 0:
            average_color = 0
        elif version == 1:
            average_color = total_g // count
        else:
            average_color = (total_r // count, total_g // count, total_b // count)
    
    return average_color

# aquí hay algún problema, me devuelve nones

def select_best_thumbnail(image_list, target_color, version):
    right_index = 0
    minimum_difference = float('inf')

    if version == 1:     
        interval_size = 255 / 30        
        right_index = int(target_color / interval_size)
        best_thumbnail = image_list[right_index]
    elif version == 2:
        
        for ind, couple in enumerate(image_list):
            temp_r, temp_g, temp_b = couple[0]            
            target_r, target_g, target_b = target_color                       
            temp_difference = math.sqrt((temp_r - target_r)**2 + (temp_g - target_g)**2 + (temp_b - target_b)**2 )

            if temp_difference < minimum_difference:                
                minimum_difference = temp_difference
                right_index = ind 

        best_thumbnail_tuple = image_list[right_index]
        best_thumbnail = best_thumbnail_tuple[1] 

    return best_thumbnail



def color_filter(image, color):    
    rgb_image = image.convert('RGB')  
    width, height = rgb_image.size    
    filter_r, filter_g, filter_b = color
    filtered_image = Image.new('RGB', (width, height))   
    original_pixels = rgb_image.load()
    filtered_pixels = filtered_image.load()    
    
    for i in range(width):
        for j in range(height):            
            original_r, original_g, original_b = original_pixels[i, j]
            new_r = (original_r + filter_r) // 2
            new_g = (original_g + filter_g) // 2
            new_b = (original_b + filter_b) // 2          
            filtered_pixels[i, j] = (new_r, new_g, new_b)
    
    return filtered_image     

                  

