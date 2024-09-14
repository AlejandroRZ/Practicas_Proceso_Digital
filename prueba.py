# Crear la imagen final rellenando con las miniaturas
                for i in range(0, recursive_image.width, tile_width):                    
                    for j in range(0, recursive_image.height, tile_height):
                        block_width = min(tile_width, recursive_image.width - i)
                        block_height = min(tile_height, recursive_image.height - j)
                        print(f'block width {block_width}')
                        print(f'block height {block_height}')
                        print(f'iteración i = {i}, j= {j}')
                        zone_grey = get_average_grey(recursive_image, i, j, block_width, block_height)
                        print(f'El gris de la región es : {zone_grey}')
                        best_thumbnail = select_best_thumbnail(image_list, zone_grey)                                    
                        pixels_bthumbnail = best_thumbnail.load()    
                        # Procesar cada pixel en el bloque
                        for m in range(block_width):
                            for n in range(block_height):
                                # Obtener las coordenadas del píxel actual
                                pixel_m = m + i
                                pixel_n = n + j                                
                                # Realiza las operaciones que necesites con cada píxel                                
                                recursive_pixels[pixel_m, pixel_n] = pixels_bthumbnail[m,n] 