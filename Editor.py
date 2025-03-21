"""
Implementación de un procesador de imágenes que aplica filtros básicos.

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 3.7
"""
from tkinter import filedialog, Tk, Frame, Label, Menu, Button, ttk, LEFT, RIGHT, BOTH, Y 
from PIL import Image, ImageTk
from functools import partial
from threading import Thread
from Filtros import FiltrosRecursivos, FiltrosColor, FiltrosConvolucion, FiltrosDithering, FiltrosArtisticos, FiltrosRedimensionar, FiltrosVarios, MarcaAgua
import tkinter as tk
import os
global html_file
html_file = None
# ########################################################## Funciones para la interfaz ########################################################## #

""" Función para cargar una imagen desde el sistema de archivos. """

def load_image():
    global original_image, displayed_image, edited_image, displayed_edited_image
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona la imagen", filetypes=[("Archivos de imagen", "*.jpg *.png"), ("JPG file", "*.jpg"), ("PNG file", "*.png")])
    
    if filename:       
        original_image = Image.open(filename) # Carga la imagen original a tamaño completo
        edited_image = original_image.copy()  # Mantén la imagen editada sin redimensionar
        displayed_image = original_image.copy()        
        displayed_edited_image = original_image.copy()  # Imagen que será redimensionada solo para mostrarla
        
        show_original_image()
        show_edited_image()
        
        root.resizable(False, False)

""" Función que ajusta la imagen cuando cambia el tamaño del frame. """

def fit_image(image, label):    
    if image:                               # Obtener el tamaño del frame correspondiente
        frame_width = label.winfo_width()
        frame_height = label.winfo_height()
        image.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)  # Redimensionar una copia de la imagen al tamaño del frame, manteniendo la relación de aspecto  
        
        img_tk = ImageTk.PhotoImage(image) # Convertir la imagen redimensionada a un objeto ImageTk
        label.configure(image=img_tk)

        label.image = img_tk  # Guardar la referencia a la imagen para que no la elimine el recolector de basura

""" Función para mostrar la imagen original redimensionada. """

def show_original_image():
    global original_image   
    if original_image:
        fit_image(displayed_image, original_lbl)

""" Función para mostrar la imagen editada redimensionada """

def show_edited_image():
    global edited_image   
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

    elif option == "Marca de agua":
        watermark_submenu.post(root.winfo_pointerx(), root.winfo_pointery())
        opened_submenu = watermark_submenu
    
    elif option == "Dithering":
        dithering_submenu.post(root.winfo_pointerx(), root.winfo_pointery())
        opened_submenu = dithering_submenu

    elif option == "Filtros artísticos":
        artistic_submenu.post(root.winfo_pointerx(), root.winfo_pointery())
        opened_submenu = artistic_submenu

    elif option == "Redimensionar imagen":
        resize_submenu.post(root.winfo_pointerx(), root.winfo_pointery())
        opened_submenu = resize_submenu

    elif option == "Otros":
        others_submenu.post(root.winfo_pointerx(), root.winfo_pointery())
        opened_submenu = others_submenu


""" Función para guardar la imagen editada."""

def save_image():
    global edited_image, html_file   
    if edited_image:        # Abre un cuadro de diálogo para guardar la imagen
        file_path = filedialog.asksaveasfilename(defaultextension=".png",   
                                                 filetypes=[("PNG file", "*.png"), ("JPG file", "*.jpg")])
        if file_path:
            edited_image.save(file_path)
            message = "Imagen guardada con éxito."  
            if html_file:
                html_path = os.path.splitext(file_path)[0] + ".html"
                with open(html_path, "w", encoding="utf-8") as html_output:
                    html_output.write(html_file)
                message = "Imagen y HTML guardados con éxito." 
                       
              
            tk.messagebox.showinfo("Guardado", message)

""" Función para evitar que más de un submenú se despliegue al mismo tiempo."""

def hide_submenu(event=None):
    global opened_submenu

    if opened_submenu:
        opened_submenu.unpost()
        opened_submenu = None

""" 
Función que define un pop up con una barra de progreso
para aquellos filtros que suelen demorarse. No se puede remidensionar
ni cerrar durante el proceso y se minimiza junto con toda
la interfaz.
"""
def progress_bar(main_window, main_window_x, main_window_y, main_window_width, main_window_height, text):
    progress_window = tk.Toplevel()
    progress_window.title(text)      
    progress_window.geometry("300x150")
    progress_window.geometry("+%d+%d" % (main_window_x + main_window_width// 3, 
                                         main_window_y + main_window_height // 3))
    progress_window.grab_set() 
    progress_window.wm_protocol("WM_DELETE_WINDOW", lambda: None)      
    progress_window.resizable(False, False)
    progress_window.wm_transient(main_window)

    label = tk.Label(progress_window, text="Procesando, por favor espere...")
    label.place(x=50, y=20)
    
    progressbar = ttk.Progressbar(progress_window, mode="indeterminate") 
    progressbar.place(x=50, y=70, width=200, height=20)
    progressbar.start() 
    
    return progress_window    
    
""" 
Función que controla la aparición de un pop up con una barra de progreso
para aquellos filtros que suelen demorarse. Permite que la función
del filtro en turno se ejecute en segundo plano.
"""  
def multi_thread_popup(target_function, function_args, main_window, text):    
    global window_x, window_y, window_width, window_height, prog_window
    prog_window = progress_bar(main_window, window_x, window_y, window_width, window_height, text)

    thread = Thread(target=target_function, args=function_args)
    thread.start()
    
    def check_thread():
        if not thread.is_alive():
            prog_window.destroy()
        else:
            prog_window.after(100, check_thread)
    
    check_thread()

""" 
Interfaz para el filtro de escala de grises.
Recibe la versión del filtro que se va a aplicar.
"""
def grey_scale_visual(version):
    global original_image   
    if original_image:
        global edited_image, displayed_edited_image, html_file

        if html_file:
            html_file = None

        edited_image = FiltrosColor.grey_scale(original_image, version)
        
        displayed_edited_image = edited_image.copy()        
        show_edited_image()

""" 
Interfaz para el filtro de mica RGB.
Recibe la versión del filtro que se va a aplicar.
"""
def rgb_glass_visual(version):
    global original_image   
    if original_image:
        global edited_image, displayed_edited_image, html_file

        if html_file:
            html_file = None

        edited_image = FiltrosColor.rgb_glass(original_image, version)

        displayed_edited_image = edited_image.copy()       
        show_edited_image()

""" 
Interfaz para los filtros por convolución.
Recibe la versión del filtro que se va a aplicar.
"""
def convolution_visual(version):
    global original_image   
    if original_image:
        global edited_image, displayed_edited_image, html_file

        if html_file:
            html_file = None

        edited_image = FiltrosConvolucion.convolution(original_image, version)

        displayed_edited_image = edited_image.copy() 
        show_edited_image()           

""" 
Interfaz para el filtro de mosaico recursivo.
Recibe la versión del filtro que se va a aplicar.
"""
def recursive_image_visual(version, main_window, text):
    global original_image   
    if original_image:           
        global html_file

        if html_file:
            html_file = None
    
        file_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona la imagen para el mosaico", filetypes=[("Archivos de imagen", "*.jpg *.png"), ("JPG file", "*.jpg"), ("PNG file", "*.png")])
        
        def recursive_generator(file_name_sec, original_image_sec):
            if file_name_sec:
                global edited_image,  displayed_edited_image 
                filler_image = Image.open(file_name)
                edited_image = FiltrosRecursivos.recursive_image_generation(original_image_sec, 
                                                                            filler_image, version, 15, 15)
                displayed_edited_image = edited_image.copy()
                
                show_edited_image()
        
        multi_thread_popup(recursive_generator, (file_name, original_image), main_window, text) 

""" 
Interfaz para el filtro que aplica una marca de agua.
Recibe la versión del filtro que se va a aplicar.
"""
def watermark_visual(version):
    global original_image   
    if original_image:        
        global edited_image, displayed_edited_image, html_file
        
        if html_file:
            html_file = None        

        file_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona la imagen para la marca", filetypes=(("JPG file","*.jpg"), ("PNG file", "*.png")))
        
        if file_name:
            watmark_image = Image.open(file_name)
            edited_image = MarcaAgua.add_image_watermark(original_image, watmark_image, version)
            displayed_edited_image = edited_image.copy()

            show_edited_image()

""" 
Interfaz para el filtro que implementa distintos tipos de dithering.
Recibe la versión del filtro que se va a aplicar.
"""
def dithering_visual(version):
   global original_image      
   if original_image:
        global edited_image, displayed_edited_image, html_file

        if html_file:
            html_file = None

        if version == 0:         
            edited_image = FiltrosDithering.semitones(original_image, 6, "white", "black")
        else:
            edited_image = FiltrosDithering.dithering(original_image, version)
            
        displayed_edited_image = edited_image.copy() 
        show_edited_image()


""" 
Interfaz para el filtro que implementa filtros artísticos.
Recibe la versión del filtro que se va a aplicar.
"""
def artistic_visual(version):
   global original_image   
   if original_image:
        global edited_image, displayed_edited_image, html_file


        if html_file:
            html_file = None

        if version == 1:         
            edited_image = FiltrosArtisticos.watercolor(original_image, 7, 1)

        elif version == 2:
            edited_image = FiltrosArtisticos.watercolor(original_image, 7, 2)
        
        elif version == 3: #Filtro de letras escala de grises
            html_file, edited_image = FiltrosArtisticos.letters_filter(original_image, 5, 9, 1)
        
        elif version == 4: #Filtro de letras en color
            html_file, edited_image = FiltrosArtisticos.letters_filter(original_image, 5, 9, 2)
        elif version == 5:
            edited_image = FiltrosArtisticos.dices_filter(original_image, 8, (0,0,0), (255,255,255))    
       
        displayed_edited_image = edited_image.copy() 
        show_edited_image()

def resize_visual(version):
   global original_image   
   if original_image:
        global edited_image, displayed_edited_image, html_file

        if html_file:
            html_file = None

        if version == 1:         
            edited_image = FiltrosRedimensionar.resize_image(original_image, 0.25)

        elif version == 2:
            edited_image =  FiltrosRedimensionar.resize_image(original_image, 0.5)
        
        elif version == 3:
            edited_image =  FiltrosRedimensionar.resize_image(original_image, 0.75)
        
        elif version == 4:
            edited_image =  FiltrosRedimensionar.resize_image(original_image, 1.5)
        
        elif version == 5:
            edited_image =  FiltrosRedimensionar.resize_image(original_image, 2)
        
        elif version == 6:
            edited_image =  FiltrosRedimensionar.resize_image(original_image, 2.5)
       
        displayed_edited_image = edited_image.copy() 
        show_edited_image()


""" 
Interfaz para el filtro que implementa filtros variados.
Recibe el tipo de filtro que se va a aplicar, indicado por un entero.
"""
def others_visual(version):
   global original_image   
   if original_image:
        global edited_image, displayed_edited_image, html_file

        if html_file:
            html_file = None

        if version == 1:         
            edited_image = FiltrosVarios.erosion(original_image, 3, 1)

        elif version == 2:
            edited_image = FiltrosVarios.erosion(original_image, 3, 2)
       
        displayed_edited_image = edited_image.copy() 
        show_edited_image()
 
   

# ########################################################## Construcción de la interfaz ########################################################## #

if __name__ == "__main__":
    global root, original_image, edited_image, displayed_image, displayed_edited_image, grey_submenu 
    global RGB_submenu, opened_submenu
    root = Tk()    
    root.title("Editor Morsa") 
    icon_path = os.path.join(os.path.dirname(__file__), "Filtros", "data", "icon.png")
    root.iconphoto(False, tk.PhotoImage(file=icon_path))
    
    # Dimensiones de la ventana
    global window_x, window_y, window_width, window_height 
    window_width = 1050
    window_height = 550    
    # Obtener el tamaño de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 3

    # Despliega la ventana principal a razón de 1/2 en el ancho y 1/3 en la altura 
    root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

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
    grey_submenu.add_command(label="Escala estandar", command=partial(multi_thread_popup, grey_scale_visual, (1,), root, "Escala estandar"))
    grey_submenu.add_command(label="Escala ponderada", command=partial(multi_thread_popup, grey_scale_visual, (2,), root, "Escala ponderada"))

    # Submenú para "Mica RGB"
    RGB_submenu = Menu(menu, tearoff=0)
    RGB_submenu.add_command(label="Mica roja", command=partial(multi_thread_popup, rgb_glass_visual, (1,), root, "Mica roja"))
    RGB_submenu.add_command(label="Mica verde", command=partial(multi_thread_popup, rgb_glass_visual, (2,), root, "Mica verde"))
    RGB_submenu.add_command(label="Mica azul", command=partial(multi_thread_popup, rgb_glass_visual, (3,), root, "Mica azul" ))

    # Submenú para "Mica RGB"
    conv_submenu = Menu(menu, tearoff=0)
    conv_submenu.add_command(label="Blur", command=partial(multi_thread_popup, convolution_visual, (1,), root, "Blur"))
    conv_submenu.add_command(label="Motion blur", command=partial(multi_thread_popup, convolution_visual, (2,), root, "Motion blur"))
    conv_submenu.add_command(label="Afinar bordes", command=partial(multi_thread_popup, convolution_visual, (3,), root, "Afinar bordes"))
    conv_submenu.add_command(label="Encontrar bordes", command=partial(multi_thread_popup, convolution_visual, (4,), root, "Encontrar bordes"))
    conv_submenu.add_command(label="Relieve", command=partial(multi_thread_popup, convolution_visual, (5,), root, "Relieve"))
    conv_submenu.add_command(label="Promedio", command=partial(multi_thread_popup, convolution_visual, (6,), root, "Promedio"))

    # Submenú para "Filtros recursivos"
    recursive_submenu = Menu(menu, tearoff=0)
    recursive_submenu.add_command(label="Recursivo grises", command=partial(recursive_image_visual, 1, root, "Recursivo grises"))
    recursive_submenu.add_command(label="Recursivo colores", command=partial(recursive_image_visual, 2, root, "Recursivo colores"))

    #Submenú para marca de agua
    watermark_submenu = Menu(menu, tearoff=0)
    watermark_submenu.add_command(label="Marca repetitiva", command=partial(multi_thread_popup, watermark_visual, (1,), root, "Marca repetitiva"))
    watermark_submenu.add_command(label="Marca centrada", command=partial(multi_thread_popup, watermark_visual, (2,), root, "Marca centrada"))
   
    #Submenú para dithering
    dithering_submenu = Menu(menu, tearoff=0)
    dithering_submenu.add_command(label="Semitonos", command=partial(multi_thread_popup, dithering_visual, (0,), root, "Semitonos"))
    dithering_submenu.add_command(label="Dithering por azar", command=partial(multi_thread_popup, dithering_visual, (1,), root, "Dithering por azar"))
    dithering_submenu.add_command(label="Dithering ordenado", command=partial(multi_thread_popup, dithering_visual, (2,), root, "Dithering ordenado"))
    dithering_submenu.add_command(label="Dithering disperso", command=partial(multi_thread_popup, dithering_visual, (3,), root, "Dithering disperso"))
    dithering_submenu.add_command(label="Floyd Steinberg", command=partial(multi_thread_popup, dithering_visual, (4,), root, "Floyd Steinberg"))

    #Submenú para filtros artísticos
    artistic_submenu = Menu(menu, tearoff=0)
    artistic_submenu.add_command(label="Acuarela a color", command=partial(multi_thread_popup, artistic_visual, (1,), root, "Acuarela a color"))
    artistic_submenu.add_command(label="Acuarela en gris", command=partial(multi_thread_popup, artistic_visual, (2,), root, "Acuarela en gris"))
    artistic_submenu.add_command(label="Letras en grises", command=partial(multi_thread_popup, artistic_visual, (3,), root, "Letras en grises"))
    artistic_submenu.add_command(label="Letras en color", command=partial(multi_thread_popup, artistic_visual, (4,), root, "Letras en color"))
    artistic_submenu.add_command(label="Mosaico de dados", command=partial(multi_thread_popup, artistic_visual, (5,), root, "Mosaico de dados"))
    
    #Submenú para filtros de redimensión
    resize_submenu = Menu(menu, tearoff=0)
    resize_submenu.add_command(label="Redimensionar al 25%", command=partial(multi_thread_popup, resize_visual, (1,), root, "Redimensionar al 25%"))
    resize_submenu.add_command(label="Redimensionar al 50%", command=partial(multi_thread_popup, resize_visual, (2,), root, "Redimensionar al 50%"))
    resize_submenu.add_command(label="Redimensionar al 75%", command=partial(multi_thread_popup, resize_visual, (3,), root, "Redimensionar al 75%"))
    resize_submenu.add_command(label="Redimensionar al 150%", command=partial(multi_thread_popup, resize_visual, (4,), root, "Redimensionar al 150%"))
    resize_submenu.add_command(label="Redimensionar al 200%", command=partial(multi_thread_popup, resize_visual, (5,), root, "Redimensionar al 200%"))
    resize_submenu.add_command(label="Redimensionar al 250%", command=partial(multi_thread_popup, resize_visual, (6,), root, "Redimensionar al 250%"))
    
    #Submenú para filtros extra
    others_submenu = Menu(menu, tearoff=0)
    others_submenu.add_command(label="Erosión de máximos", command=partial(multi_thread_popup, others_visual, (1,), root, "Erosión de máximos"))
    others_submenu.add_command(label="Erosión de míninmos", command=partial(multi_thread_popup, others_visual, (2,), root, "Erosión de míninmos"))
    
    # Agregar opciones al menú principal
    menu.add_command(label="Escala de grises", command=lambda: selected_option("Escala de grises"))
    menu.add_command(label="Mica RGB", command=lambda: selected_option("Mica RGB"))
    menu.add_command(label="Convolución", command=lambda: selected_option("Convolución"))
    menu.add_command(label="Filtros recursivos", command=lambda: selected_option("Filtros recursivos"))
    menu.add_command(label="Marca de agua", command=lambda: selected_option("Marca de agua"))
    menu.add_command(label="Dithering", command=lambda: selected_option("Dithering"))
    menu.add_command(label="Filtros artísticos", command=lambda: selected_option("Filtros artísticos"))
    menu.add_command(label="Redimensionar imagen", command=lambda: selected_option("Redimensionar imagen"))
    menu.add_command(label="Otros", command=lambda: selected_option("Otros"))

    # Variable global para almacenar la imagen original
    original_image = None
    edited_image = None
    displayed_image = None
    displayed_original_image = None   
    opened_submenu = None  # Variable global para rastrear el submenú abierto
    
    # Bind para ocultar el submenú al hacer clic en cualquier parte de la ventana
    root.bind("<Button-1>", hide_submenu)
    root.bind("<Configure>", hide_submenu)
    root.bind("<Unmap>", hide_submenu)
    root.mainloop()


   