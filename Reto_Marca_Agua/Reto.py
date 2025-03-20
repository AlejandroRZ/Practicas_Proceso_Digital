from PIL import Image
"""
Reto de remoción de una marca de agua.

Curso de proceso digital de imágenes - semestre 2025-1

Profesores:
Manuel Cristóbal López Michelone
Yessica Martínez Reyes
César Hernández Solís

Alumno:
Javier Alejandro Rivera Zavala - 311288876
"""

# Aplica un procesamiento a la imagen original para identificar y marcar áreas rojas,
# colocando las demás áreas en blanco.
def extraer_rojo(imagen_fondo):
    ancho, alto = imagen_fondo.size
    marcas_agua = Image.new("RGB", imagen_fondo.size) 
    pixeles_marca_agua = marcas_agua.load()
    pixeles_fondo = imagen_fondo.load() 

    for i in range(ancho):
        for j in range(alto):            
            r, g, b = pixeles_fondo[i, j] 

            if r > g and r > b: 
                pixeles_marca_agua[i, j] = (r, g , b)                           
            else:
                pixeles_marca_agua[i, j] = (255, 255, 255)   
   
    return marcas_agua


# Realiza una búsqueda en profundidad (DFS) en la imagen para detectar una zona conexa de píxeles no blancos.
def dfs(imagen, visitado, x, y, ancho, alto):
    imagen = imagen.convert('RGB')   
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]    
    pila = [(x, y)]
    zona_conexa = [(x, y)]
    visitado[x][y] = True
    
    while pila:
        cx, cy = pila.pop()     

        for dx, dy in direcciones:
            nx, ny = cx + dx, cy + dy  

            if 0 <= nx < ancho and 0 <= ny < alto and not visitado[nx][ny]:               
                r, g, b = imagen.getpixel((nx, ny))
               
                if (r, g, b) != (255, 255, 255):
                    visitado[nx][ny] = True
                    pila.append((nx, ny))
                    zona_conexa.append((nx, ny))
    
    return zona_conexa

# Identifica y retorna todas las zonas conexas de píxeles no blancos en la imagen.
def encontrar_zonas_conexas(imagen):    
    imagen = imagen.convert('RGB')
    ancho, alto = imagen.size   
    visitado = [[False for _ in range(alto)] for _ in range(ancho)]    
    zonas_conexas = []

    for x in range(ancho):
        for y in range(alto):            
            r, g, b = imagen.getpixel((x, y))
          
            if (r, g, b) != (255, 255, 255) and not visitado[x][y]:
                zona = dfs(imagen, visitado, x, y, ancho, alto)
                zonas_conexas.append(zona)
    
    return zonas_conexas

# Elimina las zonas conexas de la imagen que sean más pequeñas que un umbral especificado.
def eliminar_zonas_pequenas(imagen, zonas_conexas, umbral_tamano):   
    imagen = imagen.convert('RGB')    
    pixeles = imagen.load()   
    
    for zona in zonas_conexas:

        if len(zona) < umbral_tamano:

            for x, y in zona:                
                pixeles[x, y] = (255, 255, 255)
    
    return imagen

# Elimina los píxeles grises de la imagen cuyo rango de diferencia entre los valores RGB es menor que un umbral.
def eliminar_pixeles_grises(imagen, umbral_tolerancia):    
    imagen = imagen.convert('RGB')    
    pixeles = imagen.load()
    ancho, alto = imagen.size
    
    for x in range(ancho):
        for y in range(alto):
            r, g, b = pixeles[x, y]
            
            if abs(r - g) < umbral_tolerancia and abs(r - b) < umbral_tolerancia and abs(g - b) < umbral_tolerancia:                
                pixeles[x, y] = (255, 255, 255)
    
    return imagen

# Realiza una operación de barrido sobre la imagen con marca de agua, 
# reemplazando los píxeles marcados con colores (no rojos) de su vecindad.
def barrer_marca_agua(imagen_original, imagen_marca_agua, tamano_matriz):    
    imagen_original = imagen_original.convert('RGB')
    imagen_marca_agua = imagen_marca_agua.convert('RGB')    
    ancho, alto = imagen_original.size  
    imagen_resultado = imagen_original.copy()
    pixeles_resultado = imagen_resultado.load()
    pixeles_original = imagen_original.load()
    pixeles_marca_agua = imagen_marca_agua.load()
       
    for x in range(ancho):
        for y in range(alto):
            r_marca, g_marca, b_marca = pixeles_marca_agua[x, y]            
            if (r_marca, g_marca, b_marca) != (255, 255, 255):               
                color_reemplazo = obtener_color_vecinos(ancho, alto, pixeles_original, x, y, tamano_matriz)
                if color_reemplazo:
                    pixeles_resultado[x, y] = color_reemplazo
                else:
                    pixeles_resultado[x, y] = pixeles_original[x, y]
            else:
                pixeles_resultado[x, y] = pixeles_original[x, y]

    return imagen_resultado
        

# Obtiene un color promedio de los vecinos en torno a un píxel dado, si no es rojo dominante.
def obtener_color_vecinos(ancho_imagen, alto_imagen, pixeles, x, y, tamano_matriz):    
    colores = []
    
    for i in range(tamano_matriz):
        for j in range(tamano_matriz):
            posicion_vecino_x = (x - (tamano_matriz // 2) + i) % ancho_imagen
            posicion_vecino_y = (y - (tamano_matriz // 2) + j) % alto_imagen            
            r, g, b = pixeles[posicion_vecino_x, posicion_vecino_y]           
            if r <= g or r <= b:
                colores.append((r, g, b))
    no_colores = len(colores)    
    if no_colores > 0:   
        r, g, b = 0, 0, 0     
        for color in colores:
            r += color[0]
            g += color[1]
            b += color[2]
        color_adecuado = (r // no_colores, g // no_colores, b // no_colores)

        return color_adecuado
   

    return None 

# Calcula el promedio del color rojo dominante en la imagen.
def get_rojo_promedio(imagen):
    imagen = imagen.convert('RGB')
    ancho, alto = imagen.size    
    pixeles = imagen.load()
    sum_r = 0
    sum_g = 0
    sum_b = 0
    contador = 0 
    for i in range(ancho):
        for j in range(alto):            
            r, g, b = pixeles[i, j] 

            if r > g and r > b:
                sum_r += r
                sum_g += g
                sum_b += b 
                contador += 1  
    rojo_promedio = (sum_r // contador, sum_g // contador, sum_b // contador)
    print(f'rojo promedio: {rojo_promedio}')
    return rojo_promedio           

# Aplica un proceso inverso para separar la marca de agua de la imagen, ajustando el color según un promedio.
def demezclar_marca_agua(imagen_con_marca, solo_marca, color_prom, factor):
   
    imagen_con_marca = imagen_con_marca.convert('RGB')
    solo_marca = solo_marca.convert('RGB')   
    ancho, alto = imagen_con_marca.size   
    imagen_resultante = Image.new('RGB', (ancho, alto))
    pixeles_resultante = imagen_resultante.load()    
    pixeles_con_marca = imagen_con_marca.load()
    pixeles_solo_marca = solo_marca.load()
    r_prom = color_prom[0]
    g_prom = color_prom[1]
    b_prom = color_prom[2]
   
    for x in range(ancho):
        for y in range(alto):
            r_con_marca, g_con_marca, b_con_marca = pixeles_con_marca[x, y]
            r_solo_marca, g_solo_marca, b_solo_marca = pixeles_solo_marca[x, y]

            if  (r_solo_marca == 255 and g_solo_marca == 255 and b_solo_marca == 255):
                pixeles_resultante[x, y] = (r_con_marca, g_con_marca, b_con_marca)
            else:                
                r_resultante = min(255, int((r_con_marca - factor*r_prom) / (1 - factor)))
                g_resultante = min(255, int((g_con_marca - factor*g_prom) / (1 - factor)))
                b_resultante = min(255, int((b_con_marca - factor*b_prom) / (1 - factor)))
                gris = (r_resultante + g_resultante + b_resultante)//3                
                pixeles_resultante[x, y] = (gris, gris, gris)
    
    return imagen_resultante

#Ejecuta convolución dando seguimiento a una plantilla, sobre una imagen de referencia.
def convolucion_paralela(imagen_base, marca_agua, matriz_conv, factor, bias):
    if imagen_base and marca_agua:                     
        pixeles_base = imagen_base.load()
        marca_pixeles = marca_agua.load()
        altura_matriz = len(matriz_conv)
        ancho_matriz = len(matriz_conv[0])       
        imagen_resultante = Image.new("RGB", imagen_base.size)   
        pixeles_resultantes = imagen_resultante.load()

        for columna_imagen in range(imagen_base.width):
            for fila_imagen in range(imagen_base.height):

                sum_r, sum_g, sum_b = 0, 0, 0  
                if marca_pixeles[columna_imagen, fila_imagen] != (255, 255, 255):

                    for fila_matriz in range(altura_matriz):
                        for columna_matriz in range(ancho_matriz):                        
                            columna_resultante = (columna_imagen - (ancho_matriz // 2) + columna_matriz) % imagen_base.width
                            fila_resultante = (fila_imagen - (altura_matriz // 2) + fila_matriz) % imagen_base.height
                            r, g, b = pixeles_base[columna_resultante, fila_resultante]
                            sum_r += r * matriz_conv[fila_matriz][columna_matriz]
                            sum_g += g * matriz_conv[fila_matriz][columna_matriz]
                            sum_b += b * matriz_conv[fila_matriz][columna_matriz]

                    sum_r = min(max(int(factor*sum_r + bias), 0), 255)
                    sum_g = min(max(int(factor*sum_g + bias), 0), 255)
                    sum_b = min(max(int(factor*sum_b + bias), 0), 255)
                    pixeles_resultantes[columna_imagen, fila_imagen] = (sum_r, sum_g, sum_b)

                else:                  

                    pixeles_resultantes[columna_imagen, fila_imagen]  = pixeles_base[columna_imagen, fila_imagen]       

        return imagen_resultante

#Incrementa el brillo de un pixel dado un factor.  
def aumentar_brillo(r, g, b, factor):
    r = min(int(r * factor), 255)
    g = min(int(g * factor), 255)
    b = min(int(b * factor), 255)
    return r, g, b

#Incrementa el brillo de los pixeles en la zona de la marca de agua.
def incrementar_brillo_marca_agua(imagen_original, imagen_marca_agua, factor):    
    imagen_original = imagen_original.convert('RGB')
    imagen_marca_agua = imagen_marca_agua.convert('RGB')   
    ancho, alto = imagen_original.size
    imagen_resultado = imagen_original.copy()
    pixeles_resultado = imagen_resultado.load()
    pixeles_original = imagen_original.load()
    pixeles_marca_agua = imagen_marca_agua.load()
 
    for x in range(ancho):
        for y in range(alto):
            
            r_marca, g_marca, b_marca = pixeles_marca_agua[x, y]            
            if (r_marca, g_marca, b_marca) != (255, 255, 255):              
                r, g, b = pixeles_original[x, y]                
                pixeles_resultado[x, y] = aumentar_brillo(r, g, b, factor)
    
    return imagen_resultado

#Toma 2 imagenes y las combina dentro de la zona donde está la marca de agua.
def fusionar_imagenes_por_marca(imagen1, imagen2, imagen_marca_agua):
    imagen1 = imagen1.convert('RGB')
    imagen2 = imagen2.convert('RGB')
    imagen_marca_agua = imagen_marca_agua.convert('RGB')
    ancho, alto = imagen1.size
    imagen_resultado = Image.new('RGB', (ancho, alto))
    pixeles_resultado = imagen_resultado.load()
    pixeles1 = imagen1.load()
    pixeles2 = imagen2.load()
    pixeles_marca_agua = imagen_marca_agua.load()
    
    for x in range(ancho):
        for y in range(alto):            
            r_marca, g_marca, b_marca = pixeles_marca_agua[x, y] 

            if (r_marca, g_marca, b_marca) != (255, 255, 255):                
                r1, g1, b1 = pixeles1[x, y]
                r2, g2, b2 = pixeles2[x, y]               
                r_promedio = (r1 + r2) // 2
                g_promedio = (g1 + g2) // 2
                b_promedio = (b1 + b2) // 2
                pixeles_resultado[x, y] = (r_promedio, g_promedio, b_promedio)
            else:                
                pixeles_resultado[x, y] = pixeles1[x, y]
    
    return imagen_resultado

#Matrices para convolución
matriz_media= [            
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
    ]   
fact_m = 1.0 / 9.0;
bias_m = 0.0; 

matriz_bsharp = [
    [-1, -1, -1, -1, -1],
    [-1,  2,  2,  2, -1],
    [-1,  2,  8,  2, -1],
    [-1,  2,  2,  2, -1],
    [-1, -1, -1, -1, -1],
    ]
fact_bsharp = 1.0 / 8.0
bias_bsharp = 0.0



if __name__ == '__main__':
################################################################Primer reto################################################################
    imagen = Image.open("primero.jpg")
    primer_marca = extraer_rojo(imagen)
    zonas_primer_marca = encontrar_zonas_conexas(primer_marca)
    primer_marca = eliminar_zonas_pequenas(primer_marca, zonas_primer_marca, 500)
    primer_marca = eliminar_pixeles_grises(primer_marca, 12)

    zonas_primer_marca = encontrar_zonas_conexas(primer_marca)
    primer_marca = eliminar_zonas_pequenas(primer_marca, zonas_primer_marca, 12)

    imagen_reto1 = barrer_marca_agua(imagen, primer_marca, 3)
    imagen_reto1 = barrer_marca_agua(imagen_reto1, primer_marca, 3)


    primer_marca = extraer_rojo(imagen_reto1)
    zonas_primer_marca = encontrar_zonas_conexas(primer_marca)
    primer_marca = eliminar_pixeles_grises(primer_marca, 15)

    rojo_prom = get_rojo_promedio(primer_marca)
    imagen_reto1 = demezclar_marca_agua(imagen_reto1, primer_marca, rojo_prom, 0.4)
    imagen_reto1 = incrementar_brillo_marca_agua(imagen_reto1, primer_marca, 1.3)

    copia_para_mezcla = imagen_reto1.copy()
    copia_para_mezcla = convolucion_paralela(copia_para_mezcla, primer_marca, matriz_bsharp, fact_bsharp, bias_bsharp)
    imagen_reto1 = fusionar_imagenes_por_marca(imagen_reto1, copia_para_mezcla, primer_marca)
    imagen_reto1 = barrer_marca_agua(imagen_reto1, primer_marca, 3)

    imagen_reto1.save("primer_reto.png")

    ################################################################Segundo reto################################################################
    imagen2 = Image.open("segundo.jpg")
    segunda_marca = extraer_rojo(imagen2)
    zonas_segunda_marca = encontrar_zonas_conexas(segunda_marca)
    segunda_marca = eliminar_zonas_pequenas(segunda_marca, zonas_segunda_marca, 100)
    segunda_marca = eliminar_pixeles_grises(segunda_marca, 15)

    imagen_reto2 = barrer_marca_agua(imagen2, segunda_marca, 3)
    imagen_reto2 = barrer_marca_agua(imagen_reto2, segunda_marca, 3)

    segunda_marca = extraer_rojo(imagen_reto2)
    zonas_segunda_marca = encontrar_zonas_conexas(segunda_marca)
    segunda_marca = eliminar_pixeles_grises(segunda_marca, 18)
    rojo_prom2 = get_rojo_promedio(segunda_marca)
    imagen_reto2 = demezclar_marca_agua(imagen_reto2, segunda_marca, rojo_prom2, 0.8)

    imagen_reto2 = incrementar_brillo_marca_agua(imagen_reto2, segunda_marca, 2.2)

    copia_mezcla2 = imagen_reto2.copy()
    copia_mezcla2 = convolucion_paralela(copia_mezcla2, segunda_marca, matriz_bsharp, fact_bsharp, bias_bsharp)

    imagen_reto2 = convolucion_paralela(imagen_reto2, segunda_marca, matriz_media, fact_m, bias_m)
    imagen_reto2 = fusionar_imagenes_por_marca(imagen_reto2, copia_mezcla2, segunda_marca)
    imagen_reto2 = barrer_marca_agua(imagen_reto2, segunda_marca, 3)
    imagen_reto2 = barrer_marca_agua(imagen_reto2, segunda_marca, 3)
    imagen_reto2 = fusionar_imagenes_por_marca(imagen_reto2, copia_mezcla2, segunda_marca)
    imagen_reto2 = incrementar_brillo_marca_agua(imagen_reto2, segunda_marca, 1.5)


    copia_mezcla2 = imagen_reto2.copy()
    copia_mezcla2 = convolucion_paralela(copia_mezcla2, segunda_marca, matriz_bsharp, fact_bsharp, bias_bsharp)
    imagen_reto2 = barrer_marca_agua(imagen_reto2, segunda_marca, 3)
    imagen_reto2 = fusionar_imagenes_por_marca(imagen_reto2, copia_mezcla2, segunda_marca)
    imagen_reto2.save("segundo_reto.png")



    ################################################################Tercer reto################################################################
    imagen3 = Image.open("tercero.jpg")
    tercera_marca = extraer_rojo(imagen3)
    zonas_tercera_marca = encontrar_zonas_conexas(tercera_marca)
    tercera_marca = eliminar_zonas_pequenas(tercera_marca, zonas_tercera_marca, 100)
    tercera_marca = eliminar_pixeles_grises(tercera_marca, 20)
    tercera_marca = convolucion_paralela(tercera_marca, tercera_marca, matriz_media, fact_m, bias_m)
    imagen_reto3 = barrer_marca_agua(imagen3, tercera_marca, 3)
    for i in range(1):
        imagen_reto3 = barrer_marca_agua(imagen_reto3, tercera_marca, 3)

    tercera_marca = extraer_rojo(imagen_reto3)
    zonas_tercera_marca = encontrar_zonas_conexas(tercera_marca)
    tercera_marca = eliminar_pixeles_grises(tercera_marca, 23)
    rojo_prom3 = get_rojo_promedio(tercera_marca)
    imagen_reto3 = demezclar_marca_agua(imagen_reto3, tercera_marca, rojo_prom3, 0.5)
    imagen_reto3 = incrementar_brillo_marca_agua(imagen_reto3, tercera_marca, 1.7)
    copia_mezcla3 = imagen_reto3.copy()
    copia_mezcla3 = convolucion_paralela(copia_mezcla3, tercera_marca, matriz_bsharp, fact_bsharp, bias_bsharp)
    imagen_reto3 = fusionar_imagenes_por_marca(imagen_reto3, copia_mezcla3, tercera_marca)
    imagen_reto3 = convolucion_paralela(imagen_reto3, tercera_marca, matriz_media, fact_m, bias_m)
    imagen_reto3 = fusionar_imagenes_por_marca(imagen_reto3, copia_mezcla3, tercera_marca)
    imagen_reto3 = convolucion_paralela(imagen_reto3, tercera_marca, matriz_media, fact_m, bias_m)
    imagen_reto3.save("tercer_reto.png")