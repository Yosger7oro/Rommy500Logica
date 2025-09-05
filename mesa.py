from random import choice
from jugador import Jugador
from cartas import Cartas
from mazo import Mazo
from jugadas import Jugada

class Mesa:
    lista_jugadores = []
    descarte = []
    quema = []
    cartas_mesa = []
    jugadores_primera_jugada = []

    def __init__(self):
        pass

    @classmethod
    def normalizar(cls, texto):
        return texto.strip().lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

    @classmethod
    def cuantos_jugadores(cls):
        num_jugadores = int(input('¿Cuántos jugadores van a jugar?: '))
        if num_jugadores == 1:
            print('Para jugar necesitas más de un jugador.')
            return False
        elif num_jugadores > 7:
            print("Solo se puede jugar con un máximo de 7 jugadores.")
            return False
        else:
            for x in range(num_jugadores):
                nombre = input('Ingrese el nombre del jugador: ')
                jugador = Jugador(x + 1, nombre)
                cls.lista_jugadores.append(jugador)
                print('Jugador añadido.')

    @classmethod
    def mostrar_manos(cls, jugadores_reordenados, manos):
        for i, mano in enumerate(manos):
            jugador = jugadores_reordenados[i]
            print(f'\nCartas del jugador {jugador.nro_jugador} - {jugador.nombre_jugador}:')
            for carta in mano:
                print(carta)

    @classmethod
    def jugador_mano_orden(cls):
        indice_del_jugador_mano, nom_jug_mano = choice(list(enumerate(cls.lista_jugadores)))
        print(f"El jugador mano es: {nom_jug_mano.nombre_jugador}")
        jugadores_reordenados = []
        provisional = []

        for x in range(0, indice_del_jugador_mano + 1):
            jugadores_reordenados.insert(0, cls.lista_jugadores[x])

        for x in range(indice_del_jugador_mano + 1, len(cls.lista_jugadores)):
            provisional.insert(0, cls.lista_jugadores[x])

        for p in provisional:
            jugadores_reordenados.append(p)

        for x in range(len(jugadores_reordenados)):
            cls.cartas_mesa.append([])

        return jugadores_reordenados

    @classmethod
    def compra(cls, jugador_actual, jugadores, manos, mazo):
        if not cls.descarte:
            print("No hay carta en el descarte para ofrecer.")
            return

        carta_descarte = cls.descarte[-1]
        carta_comprada = False
        print(f"\nSe ofrece la carta del descarte: {carta_descarte}")

        for j in range(len(jugadores)):
            if j == jugador_actual:
                continue
            jugador_siguiente = jugadores[j]
            respuesta = input(f'{jugador_siguiente.nombre_jugador}, ¿quieres comprar la carta del descarte ({carta_descarte})? (si/no): ')

            if cls.normalizar(respuesta) == 'si':
                if mazo.cartas:
                    carta_extra = mazo.cartas.pop(-1)
                    manos[j].append(carta_descarte)
                    manos[j].append(carta_extra)
                    cls.descarte.pop(-1)
                    print(f"{jugador_siguiente.nombre_jugador} ha comprado la carta del descarte y robado una carta extra.")
                    carta_comprada = True
                else:
                    print("No hay cartas en el mazo para completar la compra.")
                break

        if not carta_comprada:
            carta_quemada = cls.descarte.pop(-1)
            cls.quema.append(carta_quemada)
            print(f"Nadie compró la carta. Se ha quemado: {carta_quemada}")

    @classmethod
    def descartar_carta(cls, jugador_actual, jugadores, manos):
        jugador = jugadores[jugador_actual]
        mano_actual = manos[jugador_actual]
        print(f"\n{jugador.nombre_jugador}, debes descartar una carta.")
        print("Tus cartas actuales:")

        # Mostrar la mano numerada
        for idx, carta in enumerate(mano_actual, 1):
            print(f"{idx}. {carta}")

        while True:
            try:
                indice = int(input("Ingresa el número de la carta que quieres descartar: "))
                if 1 <= indice <= len(mano_actual):
                    carta_a_descartar = mano_actual.pop(indice - 1)
                    cls.descarte.append(carta_a_descartar)
                    print(f"Has descartado: {carta_a_descartar}")
                    break
                else:
                    print("Número fuera de rango. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Ingresa un número.")

        manos[jugador_actual] = mano_actual

    # NUEVO MÉTODO: Mostrar menú de extensión
    @classmethod
    def mostrar_menu_extension(cls, jugador_actual, jugadores, manos, mazo):
        jugador = jugadores[jugador_actual]
        mano_actual = manos[jugador_actual]
        
        print(f"\n--- TURNO DE {jugador.nombre_jugador.upper()} ---")
        print("Cartas en la mesa:")
        for i, jugada in enumerate(cls.cartas_mesa):
            if jugada:
                print(f"Jugada {i+1}: {[str(c) for c in jugada]}")
        
        print(f"\nTus cartas: {[str(c) for c in mano_actual]}")
        
        if cls.descarte:
            print(f"Carta en el descarte: {cls.descarte[-1]}")
        else:
            print("No hay carta en el descarte.")
        
        # Reiniciar cartas usadas en extensiones para este turno
        Jugada.cartas_usadas_extension = []
        
        while True:
            print("\nOpciones:")
            print("1. Robar carta del mazo cerrado")
            print("2. Tomar carta del descarte")
            print("3. Extender jugadas existentes")
            print("4. Finalizar turno")
            
            opcion = input("Elige una opción: ")
            
            if opcion == "1":
                if mazo.cartas:
                    carta_robada = mazo.cartas.pop(-1)
                    mano_actual.append(carta_robada)
                    print(f"Has robado: {carta_robada}")
                    cls.compra(jugador_actual, jugadores, manos, mazo)
                    cls.descartar_carta(jugador_actual, jugadores, manos)
                    break
                else:
                    print("No hay cartas en el mazo cerrado.")
            elif opcion == "2":
                if cls.descarte:
                    carta_descarte = cls.descarte.pop(-1)
                    mano_actual.append(carta_descarte)
                    print(f"Has tomado del descarte: {carta_descarte}")
                    cls.descartar_carta(jugador_actual, jugadores, manos)
                    break
                else:
                    print("No hay carta en el descarte. Debes robar del mazo.")
            elif opcion == "3":
                extension_exitosa = Jugada.extender_jugadas(mano_actual, jugador, cls.cartas_mesa)
                if not extension_exitosa:
                    continue
            elif opcion == "4":
                print("Finalizando turno.")
                break
            else:
                print("Opción inválida. Intenta de nuevo.")
        
        return mano_actual

    @classmethod
    def iniciar_partida(cls):
        while cls.cuantos_jugadores() == False:
            cls.cuantos_jugadores()
        
        cantidad_de_jugadores = len(cls.lista_jugadores)
        palos = ('Pica', 'Corazon', 'Diamante', 'Trebol')
        nro_carta = ('A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K')
        
        mazo = Mazo()
        nro_mazos = mazo.calcular_nro_mazos(cantidad_de_jugadores)
        
        for _ in range(nro_mazos):
            for palo in palos:
                for carta in nro_carta:
                    cart = Cartas(carta, palo)
                    mazo.agregar_cartas(cart)
            cart = Cartas('Joker', 'Especial')
            mazo.agregar_cartas(cart)
        
        mazo.revolver_mazo()
        mazo.mostrar_cartas("Las cartas en el mazo son: ")
        mazo.mostrar_numero_cartas("El número de cartas en el mazo: ")
        
        jugadores_reordenados = cls.jugador_mano_orden()
        manos = mazo.repartir_cartas(jugadores_reordenados)
        
        if mazo.cartas:
            cls.descarte.append(mazo.cartas.pop(-1))
        
        print("Inicia el juego")
        print(f"Carta inicial en el descarte: {cls.descarte[-1]}")
        cls.mostrar_manos(jugadores_reordenados, manos)
        mazo.mostrar_cartas("Las cartas restantes en el mazo son: ")
        mazo.mostrar_numero_cartas("El número de cartas en el mazo: ")
        
        cls.jugar_partida(jugadores_reordenados, manos, mazo)

    @classmethod
    def jugar_partida(cls, jugadores, manos, mazo):
        ronda_terminada = False
        
        while not ronda_terminada:
            for i, jugador in enumerate(jugadores):
                mano_actual = manos[i]
                
                if jugador in cls.jugadores_primera_jugada:
                    # Jugador ya hizo primera jugada, mostrar menú de extensión
                    mano_actual = cls.mostrar_menu_extension(i, jugadores, manos, mazo)
                    manos[i] = mano_actual
                else:
                    # Jugador aún no ha hecho primera jugada
                    print(f"\nEs el turno de {jugador.nombre_jugador} (Jugador {jugador.nro_jugador})")
                    print("\nEs la primera ronda. Solo puedes intentar la primera jugada.")
                    print(f"Tus cartas: {[str(c) for c in mano_actual]}")
                    print(f"Las cartas en la mesa: {[str(c) for c in cls.cartas_mesa]}")
                    
                    if cls.descarte:
                        print(f"Carta en el descarte: {cls.descarte[-1]}")
                    else:
                        print("No hay carta en el descarte.")
                    
                    while True:
                        print("\nOpciones:")
                        print("1. Robar carta del mazo cerrado")
                        print("2. Tomar carta del descarte")
                        print("3. Selecciona tus cartas para bajarte")
                        
                        opcion_robar = input("Elige una opción: ")
                        
                        if opcion_robar == "1":
                            if mazo.cartas:
                                carta_robada = mazo.cartas.pop(-1)
                                mano_actual.append(carta_robada)
                                print(f"Has robado: {carta_robada}")
                                cls.compra(i, jugadores, manos, mazo)
                                cls.descartar_carta(i, jugadores, manos)
                                break
                            else:
                                print("No hay cartas en el mazo cerrado.")
                                continue
                        elif opcion_robar == "2":
                            if cls.descarte:
                                carta_descarte = cls.descarte.pop(-1)
                                mano_actual.append(carta_descarte)
                                print(f"Has tomado del descarte: {carta_descarte}")
                                cls.descartar_carta(i, jugadores, manos)
                                break
                            else:
                                print("No hay carta en el descarte. Debes robar del mazo.")
                                continue
                        elif opcion_robar == "3":
                            Jugada.validar_jugada(mano_actual, jugador, cls.cartas_mesa, cls.jugadores_primera_jugada, i)
                            if jugador not in cls.jugadores_primera_jugada:
                                continue
                            else:
                                break
                        else:
                            print("Opción inválida. Intenta de nuevo.")
                
                # Verificar si el jugador se quedó sin cartas
                if not mano_actual:
                    print(f"\n¡{jugador.nombre_jugador} se ha quedado sin cartas y ha ganado la ronda!")
                    ronda_terminada = True
                    break
            
            if ronda_terminada:
                break



            #  hola
            #  # Verificar si el jugador ya hizo su primera jugada
            #     if not jugador.primera_jugada_hecha:
            #         print("\nBuscando si tienes la primera jugada (1 trío y 1 seguidilla)...")
            #         # Llamamos a la función de jugadas.py
            #         jugada_bajada = Jugada.primera_jugada(mano_actual)

            #         if jugada_bajada:
            #             # La función devolvió una jugada, no False
            #             print("Has bajado tu primera jugada a la mesa.")
            #             jugador.primera_jugada_hecha = True # Marcamos que ya la hizo

            #             # MUY IMPORTANTE: Quitar las cartas jugadas de la mano del jugador
            #             cartas_a_quitar = []
            #             for grupo in jugada_bajada: # jugada_bajada es una lista de listas, ej: [[trio], [seguidilla]]
            #                 for carta in grupo:
            #                     cartas_a_quitar.append(carta)
                        
            #             # Creamos una nueva lista para la mano sin las cartas jugadas
            #             mano_actual_temp = [c for c in mano_actual if c not in cartas_a_quitar]
            #             mano_actual = mano_actual_temp
            #     else:
            #         # Si ya hizo la primera jugada, aquí iría la lógica para bajar más cartas (futuro)
            #         print("\nYa hiciste tu primera jugada. Ahora puedes bajar otras combinaciones.")                          
