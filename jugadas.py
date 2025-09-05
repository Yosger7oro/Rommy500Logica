from cartas import Cartas

class Jugada:
    trio = []
    seguidilla = []
    cartas_usadas_extension = []

    def __init__(self):
        pass

    @classmethod
    def agregar_cartas_primera_jugada(cls, i, lista, cartas_mesa):
        for x in lista:
            cartas_mesa[i].append(x)
        lista.clear()

    @classmethod
    def regresar_cartas(cls, lista, mano_actual):
        for x in lista:
            valor, _, palo = x.partition(" de ")
            c = Cartas(valor.strip(), palo.strip())
            mano_actual.append(c)

    @classmethod
    def eliminar_carta(cls, carta, mano_actual):
        carta_eliminada = None
        for x in mano_actual:
            if str(x).strip().lower() == carta:
                carta_eliminada = x
        if carta_eliminada:
            mano_actual.remove(carta_eliminada)

    @classmethod
    def salto_joker(cls, rango, valores):
        saltos = 0
        for i in range(rango, len(valores) - 1):
            if valores[i + 1] - valores[i] == 2:
                saltos += 1
        return saltos

    @classmethod
    def salto(cls, rango, valores):
        saltos = 0
        for i in range(rango, len(valores) - 1):
            if valores[i + 1] - valores[i] != 1:
                saltos += 1
        return saltos

    @classmethod
    def mover_joker(cls, seguidilla_ordenada):
        elemento = seguidilla_ordenada.pop(0)
        seguidilla_ordenada.append(elemento)

    @classmethod
    def jokers(cls, seguidilla_ordenada, valores, rango):
        c = 0
        for x in range(rango):
            elemento = seguidilla_ordenada.pop(0)
            insertado = 0
            for i in range(len(valores) - 1):
                actual = valores[i]
                siguiente = valores[i + 1]
                if siguiente - actual == 2 and actual != 0 and siguiente != 0 and c == 0:
                    seguidilla_ordenada.insert(i, elemento)
                    insertado = 1
                    c = 1
                    break
                elif siguiente - actual == 2 and actual != 0 and siguiente != 0 and c == 1:
                    seguidilla_ordenada.insert(i + 1, elemento)
                    insertado = 1
                    break
            if insertado == 0:
                seguidilla_ordenada.insert(0, elemento)

    @classmethod
    def opciones_joker(cls, seguidilla_ordenada, mensaje):
        print(mensaje)
        c = input("1 para colocarlo en el principio y 2 para colocarlo en el final: ")
        if c == "1":
            print("seguidilla válida")
        elif c == "2":
            cls.mover_joker(seguidilla_ordenada)
            print("seguidilla válida")

    @classmethod
    def dividir_en_grupos_validos(cls, jugada):
        grupos = []
        actual = []

        for carta in jugada:
            if isinstance(carta, str):
                valor, _, palo = carta.partition(" de ")
                carta = Cartas(valor.strip(), palo.strip())

            if not actual:
                actual.append(carta)
                continue

            primera = actual[0]

            if carta.numero == primera.numero or carta.numero == 'Joker' or primera.numero == 'Joker':
                actual.append(carta)
            elif (
                carta.figura == primera.figura and
                (
                    carta.numero == 'Joker' or
                    primera.numero == 'Joker' or
                    abs(carta.valor_numerico() - actual[-1].valor_numerico()) == 1
                )
            ):
                actual.append(carta)
            else:
                grupos.append(actual)
                actual = [carta]

        if actual:
            grupos.append(actual)

        return grupos

    @classmethod
    def puede_extender_seguidilla(cls, carta, seguidilla):
        if not all(c.figura == seguidilla[0].figura for c in seguidilla if c.numero != 'Joker'):
            return False

        valores = [c.valor_numerico() for c in seguidilla if c.numero != 'Joker']
        valores.sort()

        if carta.valor_numerico() == valores[0] - 1:
            return "inicio"
        if carta.valor_numerico() == valores[-1] + 1:
            return "final"

        return False

    @classmethod
    def puede_reemplazar_joker_trio(cls, carta, trio):
        valores = [c.numero for c in trio]
        if 'Joker' in valores:
            joker_index = valores.index('Joker')
            otros_valores = [val for i, val in enumerate(valores) if i != joker_index and val != 'Joker']
            if len(set(otros_valores)) == 1 and carta.numero == otros_valores[0]:
                return joker_index
        return -1

    @classmethod
    def puede_reemplazar_joker_seguidilla(cls, carta, seguidilla):
        joker_pos = -1
        for i, c in enumerate(seguidilla):
            if c.numero == 'Joker':
                joker_pos = i
                break

        if joker_pos == -1:
            return False

        palos = [c.figura for c in seguidilla if c.numero != 'Joker']
        if len(set(palos)) != 1 or carta.figura != palos[0]:
            return False

        seguidilla_reemplazada = seguidilla[:]
        seguidilla_reemplazada[joker_pos] = carta

        valores = [c.valor_numerico() for c in seguidilla_reemplazada]
        valores.sort()

        for i in range(len(valores) - 1):
            if valores[i + 1] - valores[i] != 1:
                return False

        return joker_pos
    @classmethod
    def extender_jugadas(cls, mano_actual, jugador, cartas_mesa):
        print("\n--- EXTENDER JUGADAS ---")
        print("Cartas en la mesa:")
        for i, jugada in enumerate(cartas_mesa):
            if jugada:
                print(f"Jugada {i+1}: {[str(c) for c in jugada]}")

        print("\nTus cartas:")
        for i, carta in enumerate(mano_actual, 1):
            print(f"{i}. {carta}")

        opciones = []

        for carta_idx, carta in enumerate(mano_actual):
            for mesa_idx, jugada in enumerate(cartas_mesa):
                if not jugada:
                    continue

                subgrupos = cls.dividir_en_grupos_validos(jugada)

                for subgrupo in subgrupos:
                    jugada_objetos = []
                    for c in subgrupo:
                        if isinstance(c, str):
                            valor, _, palo = c.partition(" de ")
                            c = Cartas(valor.strip(), palo.strip())
                        jugada_objetos.append(c)

                    if len(jugada_objetos) >= 3 and all(c.numero == jugada_objetos[0].numero for c in jugada_objetos if c.numero != 'Joker'):
                        if carta.numero == jugada_objetos[0].numero and carta not in cls.cartas_usadas_extension:
                            opciones.append((carta_idx, mesa_idx, "trio", "extender", "final", jugada_objetos))

                        joker_pos = cls.puede_reemplazar_joker_trio(carta, jugada_objetos)
                        if joker_pos != -1 and carta not in cls.cartas_usadas_extension:
                            opciones.append((carta_idx, mesa_idx, "trio", "reemplazar_joker", joker_pos, jugada_objetos))

                    elif len(jugada_objetos) >= 4 and all(c.figura == jugada_objetos[0].figura for c in jugada_objetos if c.numero != 'Joker'):
                        extension = cls.puede_extender_seguidilla(carta, jugada_objetos)
                        if extension and carta not in cls.cartas_usadas_extension:
                            opciones.append((carta_idx, mesa_idx, "seguidilla", "extender", extension, jugada_objetos))

                        joker_pos = cls.puede_reemplazar_joker_seguidilla(carta, jugada_objetos)
                        if joker_pos is not False and carta not in cls.cartas_usadas_extension:
                            opciones.append((carta_idx, mesa_idx, "seguidilla", "reemplazar_joker", joker_pos, jugada_objetos))

        if not opciones:
            print("No tienes opciones para extender jugadas.")
            return False

        print("\nOpciones de extensión:")
        for i, opcion in enumerate(opciones, 1):
            carta_idx, mesa_idx, tipo, accion, *extra, subgrupo = opcion
            carta = mano_actual[carta_idx]
            if accion == "extender":
                pos = extra[0]
                print(f"{i}. Agregar {carta} al {pos} de la {tipo} {[str(c) for c in subgrupo]}")
            else:
                joker_pos = extra[0]
                print(f"{i}. Reemplazar joker en posición {joker_pos+1} de {tipo} {[str(c) for c in subgrupo]} con {carta}")

        seleccion = input("\nSelecciona una opción (0 para cancelar): ")
        if not seleccion.isdigit() or int(seleccion) == 0:
            return False

        seleccion_idx = int(seleccion) - 1
        if seleccion_idx < 0 or seleccion_idx >= len(opciones):
            print("Opción inválida.")
            return False

        carta_idx, mesa_idx, tipo, accion, *extra, subgrupo = opciones[seleccion_idx]
        carta = mano_actual[carta_idx]

        subgrupo_objetos = []
        for c in subgrupo:
            if isinstance(c, str):
                valor, _, palo = c.partition(" de ")
                c = Cartas(valor.strip(), palo.strip())
            subgrupo_objetos.append(c)

        if accion == "extender":
            pos = extra[0]
            if pos == "inicio":
                subgrupo_objetos.insert(0, carta)
            else:
                subgrupo_objetos.append(carta)
            mano_actual.remove(carta)
            cls.cartas_usadas_extension.append(carta)
            print(f"Has agregado {carta} al {pos} de la {tipo}.")
        else:
            joker_pos = extra[0]
            joker = subgrupo_objetos[joker_pos]
            subgrupo_objetos[joker_pos] = carta
            mano_actual.remove(carta)
            mano_actual.append(joker)
            cls.cartas_usadas_extension.append(carta)
            print(f"Has reemplazado el joker con {carta}. El joker ha sido devuelto a tu mano.")

        jugada_original = cartas_mesa[mesa_idx]
        nueva_jugada = []

        for grupo in cls.dividir_en_grupos_validos(jugada_original):
            if [str(c) for c in grupo] == [str(c) for c in subgrupo]:
                nueva_jugada.extend(subgrupo_objetos)
            else:
                nueva_jugada.extend(grupo)

        cartas_mesa[mesa_idx] = nueva_jugada
        return True


            
    @classmethod
    def validar_jugada(cls,mano_actual,jugador,cartas_mesa,jugadores_primera_jugada,i):
      cls.trio.clear()
      if jugador not in jugadores_primera_jugada:
        print("primero seleccione las cartas para su trio")
        print("agregue las cartas que quiera, presione 1 para confirmar su trio, 2 para limpiar y 3 para salir")
        num_saltos=0
        carta = None
        trio_valido= False
        seguidilla_valida=False
        while carta != "1":
            mano_actual_a = [str(c) for c in mano_actual]                       
            mano_actual_a = [m.lower() for m in mano_actual_a]
            carta = input("seleccione su carta para el trio(recuerde presionar 1 para confirmar su trio): ").lower()
            if carta in mano_actual_a:
                cls.trio.append(carta)
                mano_actual_a.remove(carta)
                cls.eliminar_carta(carta,mano_actual)
            elif carta == "1":
                trioV = []
                for x in cls.trio:
                    valor, _, palo = x.partition(" de ")
                    carta_obj = Cartas(valor, palo)
                    trioV.append(carta_obj)


                if len(trioV) < 3:
                    print("Debes seleccionar al menos tres cartas para formar un trío.")
                    cls.regresar_cartas(cls.trio, mano_actual)
                    cls.trio.clear()
                    continue

                numero_de_jokers = 0
                for x, p in enumerate(trioV):
                    if p.numero == "joker" and numero_de_jokers < 1 and x != 0:
                        trioV[x].numero = trioV[0].numero
                        numero_de_jokers += 1
                    elif p.numero == "joker" and numero_de_jokers < 1 and x == 0:
                        trioV[x].numero = trioV[1].numero
                        numero_de_jokers += 1

                valores = [c.valor_numerico() for c in trioV]
                if all(v == valores[0] for v in valores):
                    trioV = [str(c) for c in trioV]
                    print(f"Trío válido: {' - '.join(trioV)}")
                    trio_valido = True
                    break

                else:
                    print("trío inválido")
                    cls.regresar_cartas(cls.trio, mano_actual)
                    cls.trio.clear()
                    continue

            elif carta=="2":
                cls.regresar_cartas(cls.trio,mano_actual)
                cls.trio.clear()  
                continue
            elif carta=="3":
                cls.regresar_cartas(cls.trio,mano_actual)
                cls.trio.clear()
                carta=1   
            else:
                print("la carta no esta :v")
        if carta != 1:
            print("ahora seleccione las cartas para su seguidilla")
            print("agregue las cartas que quiera, presione 1 para confirmar su seguidilla, 2 para limpiar y 3 para salir")
        while carta != 1:
            mano_actual_a = [str(c) for c in mano_actual]                       
            mano_actual_a = [m.lower() for m in mano_actual_a]
            carta= input("seleccione su carta para la seguidilla(recuerde presionar 1 para confirmar): ").lower()
            if carta in [x.lower() for x in mano_actual_a]:
                cls.seguidilla.append(carta)
                mano_actual_a.remove(carta)
                cls.eliminar_carta(carta,mano_actual)
            elif carta == "1":
                seguidillaV= []
                for x in cls.seguidilla:
                    valor, _, palo=x.partition(" de ")
                    c = Cartas(valor, palo)
                    seguidillaV.append(c)
                valores = [c.valor_numerico() for c in seguidillaV]
                valores= sorted(valores)
                seguidilla_ordenada = sorted(seguidillaV,key=lambda c: c.valor_numerico())
                numero_de_jokers=0
                for x, p in enumerate(seguidilla_ordenada):
                    if p.numero=="joker" and numero_de_jokers < 2:
                        seguidilla_ordenada[x].figura = seguidilla_ordenada[2].figura
                        numero_de_jokers += 1
                if all(c.figura == seguidilla_ordenada[0].figura for c in seguidilla_ordenada) and len(seguidilla_ordenada) >= 4:
                    seguidilla_ordenada = [str(c) for c in seguidilla_ordenada]
                    if valores[0] != 0 and valores[1] != 0:
                        num_saltos=cls.salto(0,valores)
                        if num_saltos == 0:
                            print(f"Seguidilla válida: {' - '.join(seguidillaV)}")
                            seguidilla_valida=True
                            break
                        else: 
                            print("seguidilla invalida, tus cartas tienen que seguir una escalera como (1,2,3,4) sin saltos como (1,2,4,5)")
                            cls.regresar_cartas(cls.seguidilla,mano_actual)
                            cls.seguidilla.clear()
                            continue
                    elif valores[0] == 0 and valores[1] != 0:
                        salto_joker1 = cls.salto_joker(1,valores)
                        if salto_joker1 == 1:      
                            cls.jokers(seguidilla_ordenada,valores,1)
                            num_saltos = cls.salto(1,valores)
                            if num_saltos == 1:
                                print("seguidilla valida")
                                seguidilla_valida=True
                                break
                            else:
                                print("seguidilla invaliada, hay mas de un salto que tu joker no puede cubrir")
                                cls.regresar_cartas(cls.seguidilla,mano_actual)
                                cls.seguidilla.clear()
                                continue
                        elif salto_joker1 == 0:
                            num_salto=cls.salto(1,valores)
                            if num_salto != 0:
                                print("seguidilla ivalida,  hay mas de un salto que tu joker no puede cubrir")
                                cls.regresar_cartas(cls.seguidilla,mano_actual)
                                cls.seguidilla.clear()
                                continue 
                            elif num_salto==0 and valores[-1] != 13 and valores[1] != 1:
                                cls.opciones_joker(seguidilla_ordenada,"deseas colocar tu joker al principio o final de tu seguidilla?")
                                seguidilla_valida=True
                                break
                            elif num_salto == 0 and valores[-1] == 13 and valores[1] != 1:
                                print("segudilla valida ")
                                seguidilla_valida=True
                                break
                            elif num_salto == 0 and valores[-1] != 13 and valores[1] == 1:
                                cls.mover_joker(seguidilla_ordenada)
                                print("seguidilla valida")
                                seguidilla_valida=True
                                break
                            elif num_salto == 0 and valores[-1] == 13 and valores[1] == 1:
                                print("seguidilla invalida, tienes mas de 13 cartas")
                                cls.regresar_cartas(cls.seguidilla,mano_actual)
                                cls.seguidilla.clear()
                                continue          
                        else:
                            print("seguidilla invalida, hay mas de un salto que tu joker no puede cubrir") 
                            cls.regresar_cartas(cls.seguidilla,mano_actual)
                            cls.seguidilla.clear()
                            continue 
                    elif valores[0] == 0 and valores[1] == 0:
                        salto_joker1 = cls.salto_joker(2,valores) 
                        if salto_joker1 == 2:
                            cls.jokers(seguidilla_ordenada,valores,2)
                            num_salto = cls.salto(2,valores)
                            if num_salto == 2:
                                print("segudilla valida")
                                seguidilla_valida=True
                                break
                            else:
                                print("seguidilla invalida, hay mas de un salto que tu joker no puede cubrir")
                                cls.regresar_cartas(cls.seguidilla,mano_actual)
                                cls.seguidilla.clear()
                                continue 
                        elif salto_joker1 == 1:
                            cls.jokers(seguidilla_ordenada,valores,1)
                            num_salto = cls.salto(2,valores) 
                            if num_salto == 1 and valores[-1] != 13 and valores[2] != 1:
                                cls.opciones_joker(seguidilla_ordenada,"deseas colocar tu joker restante al principio o final de tu seguidilla?")
                                seguidilla_valida=True
                                break
                            elif num_salto == 1 and valores[-1] == 13 and valores[2] != 1:
                                print("seguidilla valida")
                                seguidilla_valida=True
                                break
                            elif num_salto == 1 and valores[-1] != 13 and valores[2] == 1:
                                cls.mover_joker(seguidilla_ordenada)
                                print("seguidilla valida")
                                seguidilla_valida=True
                                break
                            elif num_salto == 1 and valores[-1] == 13 and valores[2] == 1:
                                print("seguidilla invalida, tienes mas 13 cartas")
                                cls.regresar_cartas(cls.seguidilla,mano_actual)
                                cls.seguidilla.clear()
                                continue 
                            else:
                                print("seguidilla invalida, hay mas de un salto que tu joker no puede cubrir")
                                cls.regresar_cartas(cls.seguidilla,mano_actual)
                                cls.seguidilla.clear()
                                continue 
                        elif salto_joker1 == 0:
                            num_salto = cls.salto(2,valores) 
                            if num_salto == 0 and valores[-1] != 13 and valores[2] != 1:
                                cls.mover_joker(seguidilla_ordenada)
                                print("segudilla valida")
                                seguidilla_valida=True
                                break

                            else:
                                print("segudilla invalida, no puedes tener dos joker seguidos")
                                cls.regresar_cartas(cls.seguidilla,mano_actual)
                                cls.seguidilla.clear()
                                continue 
                
                        else:
                            print("seguidilla invalida, hay mas de un salto que tu joker no puede cubrir")        
                            cls.regresar_cartas(cls.seguidilla,mano_actual)
                            cls.seguidilla.clear()
                            continue     
                
                        
                else:
                    print("seguidilla invalida, todas tus cartas tienen que ser del mismo palo y tienes que seleccionar mas de 4 cartas")
                    cls.regresar_cartas(cls.seguidilla,mano_actual)
                    cls.seguidilla.clear()
                    continue
            elif carta == "2":
                cls.regresar_cartas(cls.seguidilla,mano_actual)
                cls.seguidilla.clear()
                continue
            elif carta == "3":
                cls.regresar_cartas(cls.trio,mano_actual)
                cls.trio.clear()
                cls.regresar_cartas(cls.seguidilla,mano_actual)
                cls.seguidilla.clear()
                carta = 1 
            else:
                print("la carta no esta :v")
        if trio_valido == True and seguidilla_valida == True:
            cls.agregar_cartas_primera_jugada(i,trioV,cartas_mesa)
            cls.agregar_cartas_primera_jugada(i,seguidilla_ordenada,cartas_mesa)
            cls.seguidilla.clear()
            cls.trio.clear()
            jugadores_primera_jugada.append(jugador)
            print("su jugada es valida")
            print(f"las cartas que bajaste a la mesa son: {cartas_mesa[i]}")
      else:
          print("ya hiciste la primera jugada")




    # conquiste este codigo :vvvvv
    # @classmethod
    # def Trio(cls, mano):
        
    #     # Identifica todos los tríos en una mano, usando un Joker como comodín si es necesario.
    #     jokers = [carta for carta in mano if carta.numero == 'Joker']
    #     cartas_normales = [carta for carta in mano if carta.numero != 'Joker']
        
    #     conteo = {}
    #     for carta in cartas_normales:
    #         if carta.numero in conteo:
    #             conteo[carta.numero].append(carta)
    #         else:
    #             conteo[carta.numero] = [carta]
        
    #     listas_trios = []
    #     # Buscar tríos naturales (3 o más cartas iguales)
    #     numeros_usados = []
    #     for numero, cartas in conteo.items():
    #         if len(cartas) >= 3:
    #             listas_trios.append(cartas)
    #             numeros_usados.append(numero)
        
    #     # Buscar pares para completar con un Joker
    #     # Se asegura de no usar números que ya formaron un trío natural
    #     for numero, cartas in conteo.items():
    #         if numero in numeros_usados:
    #             continue
    #         # Si hay un par y tenemos un joker disponible
    #         if len(cartas) == 2 and len(jokers) > 0:
    #             # Se consume un joker para formar el trío
    #             trio_con_joker = cartas + [jokers.pop(0)]
    #             listas_trios.append(trio_con_joker)

    #     return listas_trios

    # @classmethod
    # def Seguidilla(cls, mano):
        
    #     # Identifica todas las seguidillas en una mano, usando hasta dos Jokers como comodines.
    #     rank_map = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
    #     jokers = [carta for carta in mano if carta.numero == 'Joker']
    #     cartas_normales = [carta for carta in mano if carta.numero != 'Joker']

    #     palos = {}
    #     for carta in cartas_normales:
    #         if carta.figura not in palos:
    #             palos[carta.figura] = []
    #         palos[carta.figura].append(carta)

    #     jugadas_encontradas = []
    #     # Iterar sobre cada palo para buscar seguidillas
    #     for figura, cartas_del_palo in palos.items():
    #         if len(cartas_del_palo) + len(jokers) < 4:
    #             continue
            
    #         cartas_ordenadas = sorted(cartas_del_palo, key=lambda c: rank_map[str(c.numero)])
            
    #         # Probar cada carta como un posible inicio de seguidilla
    #         for i in range(len(cartas_ordenadas)):
    #             jokers_disponibles = len(jokers)
    #             corrida_actual = [cartas_ordenadas[i]]
    #             ultimo_rank = rank_map[str(cartas_ordenadas[i].numero)]

    #             # Intentar extender la seguidilla con las demás cartas
    #             for j in range(i + 1, len(cartas_ordenadas)):
    #                 carta_siguiente = cartas_ordenadas[j]
    #                 rank_siguiente = rank_map[str(carta_siguiente.numero)]
                    
    #                 gap = rank_siguiente - ultimo_rank - 1

    #                 if gap < 0: # Misma carta o anterior, ignorar
    #                     continue
                    
    #                 # Regla: No se pueden poner 2 jokers seguidos
    #                 if gap > 1:
    #                     break # La corrida se rompe
                    
    #                 if gap <= jokers_disponibles:
    #                     jokers_disponibles -= gap
    #                     corrida_actual.append(carta_siguiente)
    #                     ultimo_rank = rank_siguiente
    #                 else:
    #                     break # No hay suficientes jokers para cubrir el hueco

    #             # Reconstruir la jugada si es válida
    #             if len(corrida_actual) > 1:
    #                 span = rank_map[str(corrida_actual[-1].numero)] - rank_map[str(corrida_actual[0].numero)] + 1
    #                 if span >= 4:
    #                     # Reconstruir la jugada completa (cartas + jokers) para mostrarla
    #                     jugada_completa = []
    #                     idx_carta_real = 0
    #                     # Se usan los jokers originales para mantener la referencia
    #                     jokers_para_jugada = [jk for jk in jokers] 
                        
    #                     for r in range(span):
    #                         rank_esperado = rank_map[str(corrida_actual[0].numero)] + r
                            
    #                         if idx_carta_real < len(corrida_actual) and rank_map[str(corrida_actual[idx_carta_real].numero)] == rank_esperado:
    #                             jugada_completa.append(corrida_actual[idx_carta_real])
    #                             idx_carta_real += 1
    #                         else:
    #                             if jokers_para_jugada:
    #                                 jugada_completa.append(jokers_para_jugada.pop(0))
                        
    #                     jugadas_encontradas.append(jugada_completa)
        
    #     # Filtrar jugadas que son subconjuntos de otras más largas
    #     if not jugadas_encontradas:
    #         return []
            
    #     jugadas_finales = []
    #     # Ordenar de más larga a más corta para una fácil filtración
    #     jugadas_encontradas.sort(key=len, reverse=True)
    #     for jugada in jugadas_encontradas:
    #         es_subconjunto = False
    #         str_jugada = set(str(c) for c in jugada)
    #         for final in jugadas_finales:
    #             str_final = set(str(c) for c in final)
    #             if str_jugada.issubset(str_final):
    #                 es_subconjunto = True
    #                 break
    #         if not es_subconjunto:
    #             jugadas_finales.append(jugada)

    #     return jugadas_finales

    # @classmethod
    # def primera_jugada(cls, mano):
        
    #     #Verifica si un jugador tiene 1 trío y 1 seguidilla para la primera jugada y le permite seleccionar cuáles usar.
    #     listas_trio = cls.Trio(mano)
    #     listas_seguidilla = cls.Seguidilla(mano)
    #     primera_jug = []

    #     if listas_trio and listas_seguidilla:
    #         print("\nTienes las cartas requeridas para la primera jugada (1 trío y 1 seguidilla).")
            
    #         print("\nTus tríos disponibles son:")
    #         for i, trio in enumerate(listas_trio):
    #             print(f"  Opción {i}: [{cls._format_card_list(trio)}]")

    #         print("\nTus seguidillas disponibles son:")
    #         for i, seguidilla in enumerate(listas_seguidilla):
    #             print(f"  Opción {i}: [{cls._format_card_list(seguidilla)}]")

    #         while True:
    #             try:
    #                 nro_trio = int(input("\nIngresa el número de la opción del trío que quieres usar: "))
    #                 if 0 <= nro_trio < len(listas_trio):
    #                     break
    #                 else:
    #                     print(f"Opción inválida. Por favor, elige un número entre 0 y {len(listas_trio) - 1}.")
    #             except ValueError:
    #                 print("Entrada inválida. Por favor, ingresa un número.")

    #         while True:
    #             try:
    #                 nro_seguidilla = int(input("Ingresa el número de la opción de la seguidilla que quieres usar: "))
    #                 if 0 <= nro_seguidilla < len(listas_seguidilla):
    #                     break
    #                 else:
    #                     print(f"Opción inválida. Por favor, elige un número entre 0 y {len(listas_seguidilla) - 1}.")
    #             except ValueError:
    #                 print("Entrada inválida. Por favor, ingresa un número.")
            
    #         primera_jug.append(listas_trio[nro_trio])
    #         primera_jug.append(listas_seguidilla[nro_seguidilla])
            
    #         print("\nHas seleccionado tus jugadas.")
    #         return primera_jug
    #     else:
    #         return False
        
    # @classmethod
    # def segunda_jugada(cls,mano):
    #     lista_seguidilla = cls.Seguidilla(mano)
    #     segunda_jug = []
    #     if(lista_seguidilla and len(lista_seguidilla) >=2):
    #         print("Felicidades, tienes lo requerido para la segunda jugada")
    #         print(f"tus seguidillas son {list(enumerate(lista_seguidilla))}")
    #         nro_seguidilla1 = int(input("Ingrese el numero de la primera seguidilla para la jugada: "))
    #         nro_seguidilla2 = int(input("Ingrese el numero de la segunda seguidilla para la jugada: "))
    #         segunda_jug.append(lista_seguidilla[nro_seguidilla1])
    #         segunda_jug.append(lista_seguidilla[nro_seguidilla2])
    #     else:
    #         return False
    #     return segunda_jug
    # def tercera_jugada(cls,mano):
    #     lista_trio = cls.Trio(mano)
    #     tercera_jug = []
    #     if(lista_trio and len(lista_trio) >=3):
    #         print("Felicidades, tienes lo requerido para la tercera jugada")
    #         print(f"tus trios son {list(enumerate(lista_trio))}")
    #         nro_trio1 = int(input("Ingrese el numero del primer trio para la jugada: "))
    #         nro_trio2 = int(input("Ingrese el numero del segundo trio para la jugada: "))
    #         nro_trio3 = int(input("Ingrese el numero del tercer trio para la jugada: "))
    #         tercera_jug.append(lista_trio[nro_trio1])
    #         tercera_jug.append(lista_trio[nro_trio2])
    #         tercera_jug.append(lista_trio[nro_trio3])
    #     else:
    #         return False
    #     return tercera_jug
    # @classmethod
    # def cuarta_jugada(cls,mano):
    #     lista_trio = cls.Trio(mano)
    #     lista_seguidilla = cls.Seguidilla(mano)
    #     cuarta_jug = []
    #     if(lista_trio and lista_seguidilla and len(lista_trio) == 2 and len(lista_seguidilla) == 1):
    #         print("Felicidades, tienes lo requerido para la cuarta jugada")
    #         print(f"tus trios son {list(enumerate(lista_trio))} y tu seguidilla son {list(enumerate(lista_seguidilla))}")
    #         nro_trio1 = int(input("Ingrese el numero del primer trio para la jugada: "))
    #         nro_trio2 = int(input("Ingrese el numero del segundo trio para la jugada: "))
    #         nro_seguidilla = int(input("Ingrese el numero de la seguidilla para la jugada: "))
    #         cuarta_jug.append(lista_trio[nro_trio1])
    #         cuarta_jug.append(lista_trio[nro_trio2])
    #         cuarta_jug.append(lista_trio[nro_seguidilla])
    #     else:
    #         return False
    #     return cuarta_jug

#aun no se sabe que se hara aqui, hay que averiguarlo jajajaj
#XD
