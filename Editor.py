"""
Implementación de un procesador de imágenes que aplica filtros básicos.

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 1.2
"""

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from functools import partial
import tkinter as tk
import os
import ProcesoRecursivo 
# ########################################################## Funciones para los filtros ########################################################## #

""" Función que implementa 2 filtros de escala de grises."""

def grey_scale(version):
    if original_image:
        # Crear una nueva imagen en modo RGB para almacenar el resultado del filtro
        grey_img = Image.new("RGB", original_image.size)

        # Obtener los datos de píxeles de la imagen original
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

        global edited_image
        edited_image = grey_img
        show_edited_image()  # Mostrar la imagen editada después de aplicar el filtro

""" Función que aplica el filtro de mica, es decir, cambia la paleta de colores 
    de la imagen por una que toma como base a un sólo color RGB."""

def RGB_glass(version):
    if original_image:
        # Crear una nueva imagen en modo RGB para almacenar el resultado del filtro
        glass_image = Image.new("RGB", original_image.size)

        # Obtener los datos de píxeles de la imagen original
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

        global edited_image
        edited_image = glass_image
        show_edited_image()  # Mostrar la imagen editada después de aplicar el filtro

""" Función que define el recorrido de una imagen pixel por pixel y aplica
    la convolución dada una matriz pertinente, además de un factor y un cesgo 
    que permiten mantener el brillo base."""

def convolution(matrix_filtr, factor, bias):
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

        global edited_image
        edited_image = convol_img
        show_edited_image()  

# Auxiliares para llamar a cada filtro en su respectivo submenú.

def blur():
    blur_matrix = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0]
    ] 
    factor = 1.0 / 13.0
    bias =  0.0 
    convolution(blur_matrix, factor, bias)

def motion_blur():
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
    convolution(mblur_matrix, factor, bias)

def border_sharp():
    bsharp_matrix = [
        [-1, -1, -1, -1, -1],
        [-1,  2,  2,  2, -1],
        [-1,  2,  8,  2, -1],
        [-1,  2,  2,  2, -1],
        [-1, -1, -1, -1, -1],
    ]
    factor = 1.0 / 8.0
    bias = 0.0
    convolution(bsharp_matrix, factor, bias)

def border_find():
    bfind_matrix = [
        [0,  0, -1,  0,  0],
        [0,  0, -1,  0,  0],
        [0,  0,  2,  0,  0],
        [0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0]
    ]
    factor = 1.0
    bias = 0.0
    convolution(bfind_matrix, factor, bias)

def emboss():
    emb_matrix = [
        [-1, -1,  0],
        [-1,  0,  1],
        [0,  1,  1]
    ]
    factor = 1.0
    bias = 128.0
    convolution(emb_matrix, factor, bias)

def mean():
    mean_matrix = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ] 
    factor = 1.0 / 9.0;
    bias = 0.0;
    convolution(mean_matrix, factor, bias)

def recursive_image_generate(val):
    if original_image:
        print("Si entré")
        global edited_image
        edited_image = ProcesoRecursivo.recursive_image_generation(val, original_image)
        show_edited_image()
        

# ########################################################## Funciones para la interfaz ########################################################## #

""" Función que abre una instancia del explorador de archivos
    del sistema, para cargar la imagen a editar."""

def load_image():
    # Exploramos en búsqueda de un archivo .png ó .jpg
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona la imagen", filetypes=(("JPG file","*.jpg"), ("PNG file", "*.png")))
    
    if filename:
        #Carga y muestra 2 instancias de la imagen, la vista original y la que muestra el filtro aplicado
        global original_image, edited_image
        original_image = Image.open(filename)
        edited_image = original_image.copy() 

        show_original_image()
        show_edited_image()

""" Función encargada de que las imagenes mostradas queden dentró de los limites del marco
    así como de redimensionarlas para que se muestren completas."""

def fit_image(img, label):
    # Obtener el tamaño del frame correspondiente
    frame_width = label.winfo_width()
    frame_height = label.winfo_height()

    # Redimensionar la imagen al tamaño del frame, manteniendo la relación de aspecto
    img.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)

    # Convertir la imagen redimensionada a un objeto ImageTk
    img_tk = ImageTk.PhotoImage(img)

    label.configure(image=img_tk)
    label.image = img_tk  # Guardar la referencia a la imagen para que no la elimine el recolector de basura.

# Vista de las imagenes.

def show_original_image():
    if original_image:
        fit_image(original_image, original_lbl)

def show_edited_image():
    if edited_image:
        fit_image(edited_image, edited_lbl)

""" Función que controla el menú de filtros disponibles."""

def selected_option(option):
    global opened_submenu
    # Ocultar el submenú previamente abierto si hay uno
    if opened_submenu:
        opened_submenu.unpost()
    
    if option == "Escala de grises":
        grey_submenu.post(root.winfo_pointerx(), root.winfo_pointery())
        opened_submenu = grey_submenu
    elif option == "Mica RGB":
        RGB_submenu.post(root.winfo_pointerx(), root.winfo_pointery())
        opened_submenu = RGB_submenu
    elif option == "Convolución":
        conv_submenu.post(root.winfo_pointerx(), root.winfo_pointery())
        opened_submenu = conv_submenu
    elif option == "Filtros recursivos":
        print('Si entré en el elif')
        recursive_submenu.post(root.winfo_pointerx(), root.winfo_pointery())
        opened_submenu = recursive_submenu



""" Función para guardar la imagen editada."""

def save_image():
    if edited_image:
        # Abre un cuadro de diálogo para guardar la imagen
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG file", "*.png"), ("JPG file", "*.jpg")])
        if file_path:
            edited_image.save(file_path)
            tk.messagebox.showinfo("Guardado", "Imagen guardada con éxito.")

""" Función para evitar que más de un submenú se despliegue al mismo tiempo."""
def hide_submenu(event=None):
    global opened_submenu
    if opened_submenu:
        opened_submenu.unpost()
        opened_submenu = None

# ########################################################## Construcción de la interfaz ########################################################## #

if __name__ == "__main__":
    global root, original_image, edited_image, grey_submenu, RGB_submenu, opened_submenu
    root = Tk()    
    root.title("Editor Morsa")    
    
    window_width = 1000
    window_height = 500

    # Obtener el tamaño de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Despliega la ventana principal a razón de 1/2 en el ancho y 1/3 en la altura 
    root.geometry(f"{window_width}x{window_height}+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 3}")

    # Frame para las imágenes (lado izquierdo de la ventana)
    image_frame = Frame(root)
    image_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Frame para la imagen original (izquierda del frame de imágenes)
    original_frame = Frame(image_frame)
    original_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    # Frame para la imagen editada (derecha del frame de imágenes)
    edited_frame = Frame(image_frame)
    edited_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    # Label para mostrar la imagen original
    original_lbl = Label(original_frame)
    original_lbl.pack(expand=True, fill=BOTH)

    # Label para mostrar la imagen editada
    edited_lbl = Label(edited_frame)
    edited_lbl.pack(expand=True, fill=BOTH)

    # Frame para los botones (lado derecho)
    button_frame = Frame(root)
    button_frame.pack(side=RIGHT, fill=Y, padx=15, pady=15)

    # Botón para seleccionar la imagen
    btn2 = Button(button_frame, text="Selecciona la imagen", command=load_image)
    btn2.pack(side=tk.TOP, fill=tk.X, pady=5)

    # Botón para guardar la imagen editada
    save_btn = Button(button_frame, text="Guardar imagen editada", command=save_image)
    save_btn.pack(side=tk.TOP, fill=tk.X, pady=5)


    # Crear el menú principal
    menu = Menu(root)
    root.config(menu=menu)

    # Submenú para "Escala de grises"
    grey_submenu = Menu(menu, tearoff=0)
    grey_submenu.add_command(label="Escala estandar", command=partial(grey_scale, 1))
    grey_submenu.add_command(label="Escala ponderada", command=partial(grey_scale, 2))

    # Submenú para "Mica RGB"
    RGB_submenu = Menu(menu, tearoff=0)
    RGB_submenu.add_command(label="Mica roja", command=partial(RGB_glass, 1))
    RGB_submenu.add_command(label="Mica verde", command=partial(RGB_glass, 2))
    RGB_submenu.add_command(label="Mica azul", command=partial(RGB_glass,3))

    # Submenú para "Mica RGB"
    conv_submenu = Menu(menu, tearoff=0)
    conv_submenu.add_command(label="Blur", command=blur)
    conv_submenu.add_command(label="Motion blur", command=motion_blur)
    conv_submenu.add_command(label="Afinar bordes", command=border_sharp)
    conv_submenu.add_command(label="Encontrar bordes", command=border_find)
    conv_submenu.add_command(label="Relieve", command=emboss)
    conv_submenu.add_command(label="Promedio", command=mean)

    # Submenú para "Filtros recursivos"
    recursive_submenu = Menu(menu, tearoff=0)
    recursive_submenu.add_command(label="Recursivo grises", command=partial(recursive_image_generate, 1))
   
    # Agregar opciones al menú principal
    menu.add_command(label="Escala de grises", command=lambda: selected_option("Escala de grises"))
    menu.add_command(label="Mica RGB", command=lambda: selected_option("Mica RGB"))
    menu.add_command(label="Convolución", command=lambda: selected_option("Convolución"))
    menu.add_command(label="Filtros recursivos", command=lambda: selected_option("Filtros recursivos"))

    # Variable global para almacenar la imagen original
    original_image = None
    edited_image = None
    opened_submenu = None  # Variable global para rastrear el submenú abierto

    # Bind para ocultar el submenú al hacer clic en cualquier parte de la ventana
    root.bind("<Button-1>", hide_submenu)
  
    root.mainloop()


   