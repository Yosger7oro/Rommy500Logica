class Jugada:
    def __init__(self):
        pass

    @staticmethod
    def _format_card_list(cards):
        """Método estático de ayuda para formatear una lista de cartas en un texto legible."""
        return ", ".join([str(c) for c in cards])

    @classmethod
    def Trio(cls, mano):
        # Identifica todos los tríos en una mano, usando un Joker como comodín si es necesario.
        #- Un trío natural son 3 o más cartas del mismo número.
        #- Un trío con comodín son 2 cartas del mismo número más 1 Joker.
        
        jokers = [carta for carta in mano if carta.numero == 'Joker']
        cartas_normales = [carta for carta in mano if carta.numero != 'Joker']
        
        conteo = {}
        for carta in cartas_normales:
            if carta.numero in conteo:
                conteo[carta.numero].append(carta)
            else:
                conteo[carta.numero] = [carta]
        
        listas_trios = []
        # Buscar tríos naturales (3 o más cartas iguales)
        numeros_usados = []
        for numero, cartas in conteo.items():
            if len(cartas) >= 3:
                listas_trios.append(cartas)
                numeros_usados.append(numero)
        
        # Buscar pares para completar con un Joker
        # Se asegura de no usar números que ya formaron un trío natural
        for numero, cartas in conteo.items():
            if numero in numeros_usados:
                continue
            # Si hay un par y tenemos un joker disponible
            if len(cartas) == 2 and len(jokers) > 0:
                # Se consume un joker para formar el trío
                trio_con_joker = cartas + [jokers.pop(0)]
                listas_trios.append(trio_con_joker)

        return listas_trios

    @classmethod
    def Seguidilla(cls, mano):
        
        # Identifica todas las seguidillas en una mano, usando hasta dos Jokers como comodines.
        #- Una seguidilla son 4 o más cartas consecutivas del mismo palo.
        #- Se pueden usar hasta 2 Jokers, pero no de forma consecutiva (ej: 5, Joker, 7, Joker, 9 es válido; 5, Joker, Joker, 8 no lo es).
        
        rank_map = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
        jokers = [carta for carta in mano if carta.numero == 'Joker']
        cartas_normales = [carta for carta in mano if carta.numero != 'Joker']

        palos = {}
        for carta in cartas_normales:
            if carta.figura not in palos:
                palos[carta.figura] = []
            palos[carta.figura].append(carta)

        jugadas_encontradas = []
        # Iterar sobre cada palo para buscar seguidillas
        for figura, cartas_del_palo in palos.items():
            if len(cartas_del_palo) + len(jokers) < 4:
                continue
            
            cartas_ordenadas = sorted(cartas_del_palo, key=lambda c: rank_map[str(c.numero)])
            
            # Probar cada carta como un posible inicio de seguidilla
            for i in range(len(cartas_ordenadas)):
                jokers_disponibles = len(jokers)
                corrida_actual = [cartas_ordenadas[i]]
                ultimo_rank = rank_map[str(cartas_ordenadas[i].numero)]

                # Intentar extender la seguidilla con las demás cartas
                for j in range(i + 1, len(cartas_ordenadas)):
                    carta_siguiente = cartas_ordenadas[j]
                    rank_siguiente = rank_map[str(carta_siguiente.numero)]
                    
                    gap = rank_siguiente - ultimo_rank - 1

                    if gap < 0: # Misma carta o anterior, ignorar
                        continue
                    
                    # Regla: No se pueden poner 2 jokers seguidos
                    if gap > 1:
                        break # La corrida se rompe
                    
                    if gap <= jokers_disponibles:
                        jokers_disponibles -= gap
                        corrida_actual.append(carta_siguiente)
                        ultimo_rank = rank_siguiente
                    else:
                        break # No hay suficientes jokers para cubrir el hueco

                # Reconstruir la jugada si es válida
                if len(corrida_actual) > 1:
                    span = rank_map[str(corrida_actual[-1].numero)] - rank_map[str(corrida_actual[0].numero)] + 1
                    if span >= 4:
                        # Reconstruir la jugada completa (cartas + jokers) para mostrarla
                        jugada_completa = []
                        idx_carta_real = 0
                        # Se usan los jokers originales para mantener la referencia
                        jokers_para_jugada = [jk for jk in jokers] 
                        
                        for r in range(span):
                            rank_esperado = rank_map[str(corrida_actual[0].numero)] + r
                            
                            if idx_carta_real < len(corrida_actual) and rank_map[str(corrida_actual[idx_carta_real].numero)] == rank_esperado:
                                jugada_completa.append(corrida_actual[idx_carta_real])
                                idx_carta_real += 1
                            else:
                                if jokers_para_jugada:
                                    jugada_completa.append(jokers_para_jugada.pop(0))
                        
                        jugadas_encontradas.append(jugada_completa)
        
        # Filtrar jugadas que son subconjuntos de otras más largas
        if not jugadas_encontradas:
            return []
            
        jugadas_finales = []
        # Ordenar de más larga a más corta para una fácil filtración
        jugadas_encontradas.sort(key=len, reverse=True)
        for jugada in jugadas_encontradas:
            es_subconjunto = False
            str_jugada = set(str(c) for c in jugada)
            for final in jugadas_finales:
                str_final = set(str(c) for c in final)
                if str_jugada.issubset(str_final):
                    es_subconjunto = True
                    break
            if not es_subconjunto:
                jugadas_finales.append(jugada)

        return jugadas_finales


    @classmethod
    def primera_jugada(cls, mano):
        
        #Verifica si un jugador tiene 1 trío y 1 seguidilla para la primera jugada y le permite seleccionar cuáles usar.
        listas_trio = cls.Trio(mano)
        listas_seguidilla = cls.Seguidilla(mano)
        primera_jug = []

        if listas_trio and listas_seguidilla:
            print("\nTienes las cartas requeridas para la primera jugada (1 trío y 1 seguidilla).")
            
            print("\nTus tríos disponibles son:")
            for i, trio in enumerate(listas_trio):
                print(f"  Opción {i}: [{cls._format_card_list(trio)}]")

            print("\nTus seguidillas disponibles son:")
            for i, seguidilla in enumerate(listas_seguidilla):
                print(f"  Opción {i}: [{cls._format_card_list(seguidilla)}]")

            while True:
                try:
                    nro_trio = int(input("\nIngresa el número de la opción del trío que quieres usar: "))
                    if 0 <= nro_trio < len(listas_trio):
                        break
                    else:
                        print(f"Opción inválida. Por favor, elige un número entre 0 y {len(listas_trio) - 1}.")
                except ValueError:
                    print("Entrada inválida. Por favor, ingresa un número.")

            while True:
                try:
                    nro_seguidilla = int(input("Ingresa el número de la opción de la seguidilla que quieres usar: "))
                    if 0 <= nro_seguidilla < len(listas_seguidilla):
                        break
                    else:
                        print(f"Opción inválida. Por favor, elige un número entre 0 y {len(listas_seguidilla) - 1}.")
                except ValueError:
                    print("Entrada inválida. Por favor, ingresa un número.")
            
            primera_jug.append(listas_trio[nro_trio])
            primera_jug.append(listas_seguidilla[nro_seguidilla])
            
            print("\nHas seleccionado tus jugadas.")
            return primera_jug
        else:
            return False
        
    @classmethod
    def segunda_jugada(cls,mano):
        lista_seguidilla = cls.Seguidilla(mano)
        segunda_jug = []
        if(lista_seguidilla and len(lista_seguidilla) >=2):
            print("Felicidades, tienes lo requerido para la segunda jugada")
            print(f"tus seguidillas son {list(enumerate(lista_seguidilla))}")
            nro_seguidilla1 = int(input("Ingrese el numero de la primera seguidilla para la jugada: "))
            nro_seguidilla2 = int(input("Ingrese el numero de la segunda seguidilla para la jugada: "))
            segunda_jug.append(lista_seguidilla[nro_seguidilla1])
            segunda_jug.append(lista_seguidilla[nro_seguidilla2])
        else:
            return False
        return segunda_jug
    def tercera_jugada(cls,mano):
        lista_trio = cls.Trio(mano)
        tercera_jug = []
        if(lista_trio and len(lista_trio) >=3):
            print("Felicidades, tienes lo requerido para la tercera jugada")
            print(f"tus trios son {list(enumerate(lista_trio))}")
            nro_trio1 = int(input("Ingrese el numero del primer trio para la jugada: "))
            nro_trio2 = int(input("Ingrese el numero del segundo trio para la jugada: "))
            nro_trio3 = int(input("Ingrese el numero del tercer trio para la jugada: "))
            tercera_jug.append(lista_trio[nro_trio1])
            tercera_jug.append(lista_trio[nro_trio2])
            tercera_jug.append(lista_trio[nro_trio3])
        else:
            return False
        return tercera_jug
    @classmethod
    def cuarta_jugada(cls,mano):
        lista_trio = cls.Trio(mano)
        lista_seguidilla = cls.Seguidilla(mano)
        cuarta_jug = []
        if(lista_trio and lista_seguidilla and len(lista_trio) == 2 and len(lista_seguidilla) == 1):
            print("Felicidades, tienes lo requerido para la cuarta jugada")
            print(f"tus trios son {list(enumerate(lista_trio))} y tu seguidilla son {list(enumerate(lista_seguidilla))}")
            nro_trio1 = int(input("Ingrese el numero del primer trio para la jugada: "))
            nro_trio2 = int(input("Ingrese el numero del segundo trio para la jugada: "))
            nro_seguidilla = int(input("Ingrese el numero de la seguidilla para la jugada: "))
            cuarta_jug.append(lista_trio[nro_trio1])
            cuarta_jug.append(lista_trio[nro_trio2])
            cuarta_jug.append(lista_trio[nro_seguidilla])
        else:
            return False
        return cuarta_jug

#aun no se sabe que se hara aqui, hay que averiguarlo jajajaj
#XD