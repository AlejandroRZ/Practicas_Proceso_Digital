"""
Proyecto final - Morsaicos.

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

Versión 1.5
"""
from tkinter import filedialog, Tk, Frame, Label, Button, ttk, messagebox, LEFT, RIGHT, BOTH, Y
from PIL import Image, ImageTk
from threading import Thread, Event
from Filtros import morsaicos
import tkinter as tk
import os

# ########################################################## Funciones para la interfaz ########################################################## #

""" Función para cargar una imagen desde el sistema de archivos. """

def load_image():
    global original_image, displayed_image
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona la imagen", filetypes=[("Archivos de imagen", "*.jpg *.png"), ("JPG file", "*.jpg"), ("PNG file", "*.png")])    
    if filename:       
        original_image = Image.open(filename) # Carga la imagen original a tamaño completo.  
        displayed_image = original_image.copy()
        show_original_image()        
        

""" 
Función que ajusta la imagen cuando cambia el tamaño del frame.

Recibe la imagen a ajustar y el marco donde está contenida.
"""

def fit_image(image, label):    
    if image:                               # Obtener el tamaño del frame correspondiente.
        frame_width = label.winfo_width()
        frame_height = label.winfo_height()
        image.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)  # Redimensionar una copia de la imagen al tamaño del frame, manteniendo la relación de aspecto.  
        img_tk = ImageTk.PhotoImage(image) # Convertir la imagen redimensionada a un objeto ImageTk.
        label.configure(image=img_tk)
        label.image = img_tk  # Guardar la referencia a la imagen para que no la elimine el recolector de basura.

""" Función para mostrar la imagen original redimensionada. """

def show_original_image():
    global original_image   
    if original_image:
        fit_image(displayed_image, original_lbl)

""" Función envoltorio que permite detener la ejecución del proceso de la biblioteca."""
def cancelable_process_image_library(cancel_event):    
    # Verificar cancelación periódicamente.          
    if cancel_event.is_set():                
        return                
    biblioteca = "./Filtros/data/Biblioteca"    
    morsaicos.save_average_colors(biblioteca, "./Filtros/data/colors.txt")   

    
""" Función envoltorio permite detener la ejecución de la generación del mosaico."""
def cancelable_generate_mosaic(cancel_event):   
    global original_image
    if original_image:

        if cancel_event.is_set():   # Verificar cancelación periódicamente.             
            return    
        colors = "./Filtros/data/colors.txt" 
        
        with open(colors, "r") as file:
            mosaic = morsaicos.process_image_to_mosaic(original_image, colors, 8, "./Filtros/data/Biblioteca", 1)   #Acá se puede cambiar la medida. 
                
        with open("morsaico.html", "w", encoding="utf-8") as html_output:
            html_output.write(mosaic)
        
        
        
""" 
Función que controla los procesos de análisis de la biblioteca de imágenes 
así como la generación del mosaico.

Genera un pop up que indica el avance del proceso y contiene botones para 
abortar el mismo.

Recibe la versión del proceso a controlar, 1 para analizar la biblitoeca y 2
para generar el mosaico.
"""
def process_control(version):
    global root, original_image, window_x, window_y, window_width, window_height
    if original_image:
        cancel_event = Event()  #Preparamos evento para cancelar de así requerirlo.

        progress_window = tk.Toplevel() #Generamos pop up con barra de progreso.
        progress_window.title("Morsaicos")            
        progress_window.geometry("300x150")
        progress_window.geometry("+%d+%d" % (window_x + window_width// 3, 
                                            window_y + window_height // 3))
        progress_window.grab_set() 
        progress_window.wm_protocol("WM_DELETE_WINDOW", lambda: None)      
        progress_window.resizable(False, False)
        progress_window.wm_transient(root)
        progress = None 
                        #Determinamos el texto adecuado.
        if version == 1:
            progress = "Analizando la biblioteca, por favor espere ..."
        elif version == 2:
            progress = "Generando morsaico, por favor espere ..."

        label = tk.Label(progress_window, text=progress)
        label.pack(pady=10)

        progressbar = ttk.Progressbar(progress_window, mode="indeterminate") 
        progressbar.place(x=50, y=45, width=200, height=20)
        progressbar.start() 

        cancel_button = tk.Button(progress_window, text="Cancelar",  #Añadimos botón para abortar proceso.
                                command=lambda: on_close(), width=5, height=3)
        cancel_button.pack(pady=30)

        def run_process():      #Función interna que corre el proceso correspondiende.
            try:

                message = None
                if version == 1:
                    message = "No se pudo procesar la biblioteca"
                    cancelable_process_image_library(cancel_event)
                    progress_window.destroy()
                elif version == 2:
                    message = "No se pudo generar el mosaico"
                    cancelable_generate_mosaic(cancel_event)
                    progress_window.destroy()
            except Exception as e:

                progress_window.destroy()
                messagebox.showerror("Error", f"{message}: {e}") #Mensaje con el error.                

        thread = Thread(target=run_process) #Ejecuta el proceso en paralelo al pop up.
        thread.start()
                                    
        def on_close():     # Cerrar ventana también cancela el proceso.
            cancel_event.set()
            progress_window.destroy()           
   
        progress_window.protocol("WM_DELETE_WINDOW", on_close)  

"""
Funciones envoltorio para pasar como comando a los botonesp pertinentes.

La primera es para el análisis de la biblioteca de imágenes y la segunda
para la generación del mosaico.
"""

def process_library():
    process_control(1)

def generate_mosaic():
    process_control(2)
        


# ########################################################## Construcción de la interfaz ########################################################## #

if __name__ == "__main__":
    global root, original_image, displayed_image, mosaic, prog_window    
    root = Tk()    
    root.title("Morsaicos") 
    icon_path = os.path.join(os.path.dirname(__file__), "Filtros", "data", "icon.png")
    root.iconphoto(False, tk.PhotoImage(file=icon_path))
    
    # Dimensiones de la ventana.
    global window_x, window_y, window_width, window_height 
    window_width = 750
    window_height = 550    
    # Obtener el tamaño de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 3

    # Despliega la ventana principal a razón de 1/2 en el ancho y 1/3 en la altura. 
    root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    # Frame para las imágenes (lado izquierdo de la ventana).
    image_frame = Frame(root)
    image_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Frame para la imagen original (izquierda del frame de imágenes).
    original_frame = Frame(image_frame)
    original_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

   
    # Label para mostrar la imagen original.
    original_lbl = Label(original_frame)
    original_lbl.pack(expand=True, fill=BOTH)
   
    # Frame para los botones (lado derecho).
    button_frame = Frame(root)
    button_frame.pack(side=RIGHT, fill=Y, padx=15, pady=15)

    # Botón para seleccionar la imagen.
    btn2 = Button(button_frame, text="Selecciona la imagen", command=load_image)
    btn2.pack(side=tk.TOP, fill=tk.X, pady=5)   
   
    # Botón para analizar la biblioteca.
    save_btn = Button(button_frame, text="Analizar biblioteca", command=process_library)
    save_btn.pack(side=tk.TOP, fill=tk.X, pady=5)

    # Botón para guardar la imagen editada.
    save_btn = Button(button_frame, text="Generar morsaico", command=generate_mosaic)
    save_btn.pack(side=tk.TOP, fill=tk.X, pady=5)
    
    # Iniciamos variables globales.
    original_image = None    
    displayed_image = None 
    mosaic = None  
    
    root.resizable(False, False) #Cancelamos cambios en las dimensiones.
  
    root.mainloop()


   