Implementación de un procesador de imágenes que genera mosaicos empleando otras imágenes.

Curso de proceso digital de imágenes - semestre 2025-1

Proyecto final - Morsaicos

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876

RESUMEN

- Para ejecutar el proyecto basta con posicionarse dentro de la carpeta "Morsaicos" desde la terminal y emplear el comando "python interfaz.py" o bien echar a andar el proyecto en el archivo "interfaz.py" desde su editor de texto/entorno de desarrollo favorito. 

Además de las bibliotecas básicas de python, este proyecto emplea tkinter y pillow, quizás también alguna otra que no recuerdo en este momento, así que por favor añadanlas a su entorno.

El proyecto ofrece una interfaz simple que permite visualizar la imagen a procesar y da 3 opciones, cargar la imagen, analizar la biblioteca y generar el mosaico.

- CARGAR IMAGEN: Permite cargar y visualizar imágenes .png y .jpg para ser procesadas, pueden seleccionar dentro de su equipo la que gusten.

- ANALIZAR BIBLIOTECA: Para poder generar el mosaico, es preciso analizar primero la biblioteca de imágenes, las imágenes deben de guardarse en la carpeta Morsaicos/Filtros/data/Biblioteca que ya está incluida en el proyecto pero que se encuentra vacía por motivos de espacio, ahí deben de copiar la biblioteca de imágenes que prefieran, yo utilice la del archivo descargable https://www.mediafire.com/file/0xajdoeqk97cg4o/photos-800000.rar/file 

Si el programa no encuentra la carpeta, mostrará un pop up con un mensaje de error, si la biblioteca está vacía, generará un .txt vacío. Si la carpeta existe y tiene algún contenido, el programa generará después de un rato (más largo conforme más grande sea la biblioteca) un archivo llamado "colors.txt" donde se vierte la información recopilada, esto dentro de la carpeta Morsaicos/Filtros/data; dicho archivo será leído para generar el mosaico. El proceso puede ser cancelado en cualquier momento dando click en el botón "cancelar" del pop up del progreso, el resultado será un .txt con información de las imágenes que alcanzo a procesar.

- GENERAR MORSAICO: 

Para esta etapa es necesario haber generado el .txt con la información de la biblioteca procesada, de no haber generado el .txt, el programa lanzará un pop up con el mensaje de error, si se genera un .txt vacío en la etapa anterior, ya sea por cancelación prematura o biblioteca vacía, también se mostrará un mensaje de error.

Si se cuenta con el .txt generado pero por algún motivo se borra la biblioteca de imágenes, aún así podrá generarse el .html con el mosaico aunque, al intentar abrirlo en el navegador, no podrá visualizarse su contenido. El mosaico se guarda como "morsaico.html" dentro de la carpeta de origen "Morsaicos", el html contiene rutas relativas a partir de ahí para buscar las imágenes. Dichas rutas y todas las demás empleadas en el programa pueden ser modificadas a conveniencia, así mismo, en el archivo "interfaz.py" el parámetro "version" para la función "morsaicos.process_image_to_mosaic" puede ser cambiado, version = 1 es para distancia euclideana y version = 2 es para distancia Riemersma, por defecto tiene la medida euclideana. Para más información al respecto, la documentación del código aclara todos los detalles.

Adjunto una carpeta con evidencias y resultados del programa en turno, también adjunto un archivo "colors.txt" con el resultado de haber procesado la biblioteca del descargable ya mencionado, para que así eviten tener que efectuar todo el proceso, ya que el mismo es largo. Copien dentro de la carpeta "Biblioteca" las imágenes indicadas para visualizar los .html que generen. Además de lo anterior, incluyo dentro de la carpeta de evidencias 2 archivos .html generados con las 2 medidas, euclideana y riemersma, y la biblioteca mencionada, para visualizarlos copienlos dentro de la carpeta "Morsaicos" y abranlos desde su navegador de preferencia. 


