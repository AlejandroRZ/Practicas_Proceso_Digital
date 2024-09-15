"""
Implementación de un procesador de imágenes que aplica filtros básicos.

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 1.5
"""
from tkinter import filedialog, Tk, Frame, Label, Menu, Button, LEFT, RIGHT, BOTH, Y 
from PIL import Image, ImageTk
from functools import partial
import tkinter as tk
import os
import FiltrosRecursivos, FiltrosBasicos, FiltrosConvolucion 

# ########################################################## Funciones para la interfaz ########################################################## #


def load_image():
    global original_image, displayed_image, edited_image, displayed_edited_image
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona la imagen", filetypes=(("JPG file","*.jpg"), ("PNG file", "*.png")))
    
    if filename:
        # Carga la imagen original a tamaño completo
        original_image = Image.open(filename)
        edited_image = original_image.copy()  # Mantén la imagen editada sin redimensionar
        displayed_image = original_image.copy()
        displayed_edited_image = original_image.copy()  # Imagen que será redimensionada solo para mostrarla

        show_original_image()
        show_edited_image()
        root.resizable(False, False)

# Función que ajusta la imagen cuando cambia el tamaño del frame
def fit_image(image, label):
    if image:
        # Obtener el tamaño del frame correspondiente
        frame_width = label.winfo_width()
        frame_height = label.winfo_height()

        # Redimensionar una copia de la imagen al tamaño del frame, manteniendo la relación de aspecto        
        image.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)

        # Convertir la imagen redimensionada a un objeto ImageTk
        img_tk = ImageTk.PhotoImage(image)

        label.configure(image=img_tk)
        label.image = img_tk  # Guardar la referencia a la imagen para que no la elimine el recolector de basura.

# Función para mostrar la imagen original redimensionada
def show_original_image():
    if original_image:
        fit_image(displayed_image, original_lbl)

# Función para mostrar la imagen editada redimensionada
def show_edited_image():
    if edited_image:
        fit_image(displayed_edited_image, edited_lbl)


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

def grey_scale_visual(version):
    global edited_image, displayed_edited_image
    edited_image = FiltrosBasicos.grey_scale(original_image, version)
    displayed_edited_image = edited_image.copy()
    show_edited_image()

def rgb_glass_visual(version):
    global edited_image, displayed_edited_image
    edited_image = FiltrosBasicos.rgb_glass(original_image, version)
    displayed_edited_image = edited_image.copy()
    show_edited_image()

def convolution_visual(version):
    global edited_image, displayed_edited_image
    edited_image = FiltrosConvolucion.convolution(original_image, version)
    displayed_edited_image = edited_image.copy()
    show_edited_image()

def recursive_image_visual(version):
    if original_image:        
        global edited_image,  displayed_edited_image
        edited_image = FiltrosRecursivos.recursive_image_generation(version, original_image)
        displayed_edited_image = edited_image.copy()
        show_edited_image()



# ########################################################## Construcción de la interfaz ########################################################## #

if __name__ == "__main__":
    global root, original_image, edited_image, displayed_image, displayed_edited_image, grey_submenu, RGB_submenu, opened_submenu
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
    grey_submenu.add_command(label="Escala estandar", command=partial(grey_scale_visual, 1))
    grey_submenu.add_command(label="Escala ponderada", command=partial(grey_scale_visual, 2))

    # Submenú para "Mica RGB"
    RGB_submenu = Menu(menu, tearoff=0)
    RGB_submenu.add_command(label="Mica roja", command=partial(rgb_glass_visual, 1))
    RGB_submenu.add_command(label="Mica verde", command=partial(rgb_glass_visual, 2))
    RGB_submenu.add_command(label="Mica azul", command=partial(rgb_glass_visual,3))

    # Submenú para "Mica RGB"
    conv_submenu = Menu(menu, tearoff=0)
    conv_submenu.add_command(label="Blur", command=partial(convolution_visual, 1))
    conv_submenu.add_command(label="Motion blur", command=partial(convolution_visual, 2))
    conv_submenu.add_command(label="Afinar bordes", command=partial(convolution_visual, 3))
    conv_submenu.add_command(label="Encontrar bordes", command=partial(convolution_visual, 4))
    conv_submenu.add_command(label="Relieve", command=partial(convolution_visual, 5))
    conv_submenu.add_command(label="Promedio", command=partial(convolution_visual, 6))

    # Submenú para "Filtros recursivos"
    recursive_submenu = Menu(menu, tearoff=0)
    recursive_submenu.add_command(label="Recursivo grises", command=partial(recursive_image_visual, 1))
    recursive_submenu.add_command(label="Recursivo colores", command=partial(recursive_image_visual, 2))
   
    # Agregar opciones al menú principal
    menu.add_command(label="Escala de grises", command=lambda: selected_option("Escala de grises"))
    menu.add_command(label="Mica RGB", command=lambda: selected_option("Mica RGB"))
    menu.add_command(label="Convolución", command=lambda: selected_option("Convolución"))
    menu.add_command(label="Filtros recursivos", command=lambda: selected_option("Filtros recursivos"))

    # Variable global para almacenar la imagen original
    original_image = None
    edited_image = None
    displayed_image = None
    displayed_original_image = None   
    opened_submenu = None  # Variable global para rastrear el submenú abierto

    # Bind para ocultar el submenú al hacer clic en cualquier parte de la ventana
    root.bind("<Button-1>", hide_submenu)
  
    root.mainloop()


   