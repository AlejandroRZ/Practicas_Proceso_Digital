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


# ########################################################## Funciones para los filtros ########################################################## #

""" Función que implementa 2 filtros de escala de grises."""

def escala_grises(version):
    if img_original:
        # Crear una nueva imagen en modo RGB para almacenar el resultado del filtro
        img_grises = Image.new("RGB", img_original.size)

        # Obtener los datos de píxeles de la imagen original
        pixels = img_original.load()
        pixels_grises = img_grises.load()

        # Recorre la imagen pixel a pixel y les aplica la formula de la media ó de la media
        # ponderada para convertir a escala de grises.        
        for i in range(img_original.width):
            for j in range(img_original.height):
                r, g, b = pixels[i, j]
                gris = (r + g + b) // 3
                if version == 2:
                    gris = int(r*0.299 + g*0.587 + b*0.114)
                pixels_grises[i, j] = (gris, gris, gris)

        global img_editada
        img_editada = img_grises
        mostrar_imagen_editada()  # Mostrar la imagen editada después de aplicar el filtro

""" Función que aplica el filtro de mica, es decir, cambia la paleta de colores 
    de la imagen por una que toma como base a un sólo color RGB."""

def mica_RGB(version):
    if img_original:
        # Crear una nueva imagen en modo RGB para almacenar el resultado del filtro
        img_mica = Image.new("RGB", img_original.size)

        # Obtener los datos de píxeles de la imagen original
        pixels = img_original.load()
        pixels_rgb = img_mica.load()

        # Recorre la imagen pixel a pixel y mantiene únicamente un valor de los bytes RGB
        # los 2 restantes los establece en cero.  
        for i in range(img_original.width):
            for j in range(img_original.height):
                r, g, b = pixels[i, j]
                if version == 1:
                    pixels_rgb[i, j] = (r, 0, 0)
                elif version == 2:
                    pixels_rgb[i, j] = (0, g, 0)
                else:
                    pixels_rgb[i, j] = (0, 0, b)

        global img_editada
        img_editada = img_mica
        mostrar_imagen_editada()  # Mostrar la imagen editada después de aplicar el filtro

""" Función que define el recorrido de una imagen pixel por pixel y aplica
    la convolución dada una matriz pertinente, además de un factor y un cesgo 
    que permiten mantener el brillo base."""

def convolucion(matriz_filtr, factor, bias):
    if img_original:
        img_convol = Image.new("RGB", img_original.size)        
        pixels = img_original.load()
        pixels_conv = img_convol.load()
        matrix_height = len(matriz_filtr)
        matrix_width = len(matriz_filtr[0])       
        

        for columna_img in range(img_original.width):
            for fila_img in range(img_original.height):

                sum_r, sum_g, sum_b = 0, 0, 0  
                
                for fila_matriz in range(matrix_height):
                    for columna_matriz in range(matrix_width):                        

                        # Calcular la posición del píxel en la imagen
                        columna_prod = (columna_img - (matrix_width // 2) + columna_matriz) % img_original.width
                        fila_prod = (fila_img - (matrix_height // 2) + fila_matriz) % img_original.height
                        
                        # Obtener el valor del píxel correspondiente
                        r, g, b = pixels[columna_prod, fila_prod]

                        # Aplicar el filtro (convolución)
                        sum_r += r * matriz_filtr[fila_matriz][columna_matriz]
                        sum_g += g * matriz_filtr[fila_matriz][columna_matriz]
                        sum_b += b * matriz_filtr[fila_matriz][columna_matriz]

                # Asegurarse de que los valores de los píxeles estén en el rango correcto [0, 255]
                sum_r = min(max(int(factor*sum_r + bias), 0), 255)
                sum_g = min(max(int(factor*sum_g + bias), 0), 255)
                sum_b = min(max(int(factor*sum_b + bias), 0), 255)

                # Asignar el nuevo valor al píxel convolucionado
                pixels_conv[columna_img, fila_img] = (sum_r, sum_g, sum_b)         

        global img_editada
        img_editada = img_convol
        mostrar_imagen_editada()  

# Auxiliares para llamar a cada filtro en su respectivo submenú.

def blur():
    matriz_blur = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0]
    ] 
    factor = 1.0 / 13.0
    bias =  0.0 
    convolucion(matriz_blur, factor, bias)

def motion_blur():
    matriz_mblur= [
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
    convolucion(matriz_mblur, factor, bias)

def border_sharp():
    matriz_bsharp = [
        [-1, -1, -1, -1, -1],
        [-1,  2,  2,  2, -1],
        [-1,  2,  8,  2, -1],
        [-1,  2,  2,  2, -1],
        [-1, -1, -1, -1, -1],
    ]
    factor = 1.0 / 8.0
    bias = 0.0
    convolucion(matriz_bsharp, factor, bias)

def border_find():
    matriz_find = [
        [0,  0, -1,  0,  0],
        [0,  0, -1,  0,  0],
        [0,  0,  2,  0,  0],
        [0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0]
    ]
    factor = 1.0
    bias = 0.0
    convolucion(matriz_find, factor, bias)

def emboss():
    matriz_emb = [
        [-1, -1,  0],
        [-1,  0,  1],
        [0,  1,  1]
    ]
    factor = 1.0
    bias = 128.0
    convolucion(matriz_emb, factor, bias)

def mean():
    matriz_mean = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ] 
    factor = 1.0 / 9.0;
    bias = 0.0;
    convolucion(matriz_mean, factor, bias)


# ########################################################## Funciones para la interfaz ########################################################## #

""" Función que abre una instancia del explorador de archivos
    del sistema, para cargar la imagen a editar."""

def cargar_imagen():
    # Exploramos en búsqueda de un archivo .png ó .jpg
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona la imagen", filetypes=(("JPG file","*.jpg"), ("PNG file", "*.png")))
    
    if filename:
        #Carga y muestra 2 instancias de la imagen, la vista original y la que muestra el filtro aplicado
        global img_original, img_editada
        img_original = Image.open(filename)
        img_editada = img_original.copy() 

        mostrar_imagen_original()
        mostrar_imagen_editada()

""" Función encargada de que las imagenes mostradas queden dentró de los limites del marco
    así como de redimensionarlas para que se muestren completas."""

def ajustar_imagen(img, label):
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

def mostrar_imagen_original():
    if img_original:
        ajustar_imagen(img_original, lbl_original)

def mostrar_imagen_editada():
    if img_editada:
        ajustar_imagen(img_editada, lbl_editado)

""" Función que controla el menú de filtros disponibles."""

def opcion_seleccionada(opcion):
    global submenu_abierto
    # Ocultar el submenú previamente abierto si hay uno
    if submenu_abierto:
        submenu_abierto.unpost()
    
    if opcion == "Escala de grises":
        submenu_grises.post(root.winfo_pointerx(), root.winfo_pointery())
        submenu_abierto = submenu_grises
    elif opcion == "Mica RGB":
        submenu_RGB.post(root.winfo_pointerx(), root.winfo_pointery())
        submenu_abierto = submenu_RGB
    elif opcion == "Convolución":
        submenu_Conv.post(root.winfo_pointerx(), root.winfo_pointery())
        submenu_abierto = submenu_Conv

""" Función para guardar la imagen editada."""

def guardar_imagen():
    if img_editada:
        # Abre un cuadro de diálogo para guardar la imagen
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG file", "*.png"), ("JPG file", "*.jpg")])
        if file_path:
            img_editada.save(file_path)
            tk.messagebox.showinfo("Guardado", "Imagen guardada con éxito.")

""" Función para evitar que más de un submenú se despliegue al mismo tiempo."""
def ocultar_submenu(event=None):
    global submenu_abierto
    if submenu_abierto:
        submenu_abierto.unpost()
        submenu_abierto = None

# ########################################################## Entrada en ejecución ########################################################## #

if __name__ == "__main__":
    global root, img_original, img_editada, submenu_grises, submenu_RGB, submenu_abierto
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
    frame_imagenes = Frame(root)
    frame_imagenes.pack(side=LEFT, fill=BOTH, expand=True)

    # Frame para la imagen original (izquierda del frame de imágenes)
    frame_original = Frame(frame_imagenes)
    frame_original.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    # Frame para la imagen editada (derecha del frame de imágenes)
    frame_editado = Frame(frame_imagenes)
    frame_editado.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    # Label para mostrar la imagen original
    lbl_original = Label(frame_original)
    lbl_original.pack(expand=True, fill=BOTH)

    # Label para mostrar la imagen editada
    lbl_editado = Label(frame_editado)
    lbl_editado.pack(expand=True, fill=BOTH)

    # Frame para los botones (lado derecho)
    frame_boton = Frame(root)
    frame_boton.pack(side=RIGHT, fill=Y, padx=15, pady=15)

    # Botón para seleccionar la imagen
    btn2 = Button(frame_boton, text="Selecciona la imagen", command=cargar_imagen)
    btn2.pack(side=tk.TOP, fill=tk.X, pady=5)

    # Botón para guardar la imagen editada
    btn_guardar = Button(frame_boton, text="Guardar imagen editada", command=guardar_imagen)
    btn_guardar.pack(side=tk.TOP, fill=tk.X, pady=5)


    # Crear el menú principal
    menu = Menu(root)
    root.config(menu=menu)

    # Submenú para "Escala de grises"
    submenu_grises = Menu(menu, tearoff=0)
    submenu_grises.add_command(label="Escala estandar", command=partial(escala_grises, 1))
    submenu_grises.add_command(label="Escala ponderada", command=partial(escala_grises, 2))

    # Submenú para "Mica RGB"
    submenu_RGB = Menu(menu, tearoff=0)
    submenu_RGB.add_command(label="Mica roja", command=partial(mica_RGB, 1))
    submenu_RGB.add_command(label="Mica verde", command=partial(mica_RGB, 2))
    submenu_RGB.add_command(label="Mica azul", command=partial(mica_RGB,3))

    # Submenú para "Mica RGB"
    submenu_Conv = Menu(menu, tearoff=0)
    submenu_Conv.add_command(label="Blur", command=blur)
    submenu_Conv.add_command(label="Motion blur", command=motion_blur)
    submenu_Conv.add_command(label="Afinar bordes", command=border_sharp)
    submenu_Conv.add_command(label="Encontrar bordes", command=border_find)
    submenu_Conv.add_command(label="Relieve", command=emboss)
    submenu_Conv.add_command(label="Promedio", command=mean)

    # Agregar opciones al menú principal
    menu.add_command(label="Escala de grises", command=lambda: opcion_seleccionada("Escala de grises"))
    menu.add_command(label="Mica RGB", command=lambda: opcion_seleccionada("Mica RGB"))
    menu.add_command(label="Convolución", command=lambda: opcion_seleccionada("Convolución"))

    # Variable global para almacenar la imagen original
    img_original = None
    img_editada = None
    submenu_abierto = None  # Variable global para rastrear el submenú abierto

    # Bind para ocultar el submenú al hacer clic en cualquier parte de la ventana
    root.bind("<Button-1>", ocultar_submenu)

    root.mainloop()