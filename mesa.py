from random import choice
from jugador import Jugador
from cartas import Cartas
from mazo import Mazo

class Mesa:
    lista_jugadores = []
    descarte = []
    
    def __init__(self):
        pass
        
    @classmethod
    def cuantos_jugadores(cls):
        num_jugadores = int(input('Cuantos jugadores van a jugar?: '))
        if num_jugadores == 1:
            print('Para jugar necesitas mas de un jugador')
            return False
        elif num_jugadores > 7:
            print("Solo se puede jugar de maximo 7 jugadores")
            return False
        else:
            for x in range(num_jugadores):
                nombre = input('Ingrese el nombre del jugador: ')
                jugador = Jugador(x+1, nombre)
                cls.lista_jugadores.append(jugador)
                print('jugador añadido')
    @classmethod
    def mostrar_manos(cls, jugadores_reordenados, manos):
        for i, mano in enumerate(manos):
            jugador = jugadores_reordenados[i]
            print(f'\nCartas del jugador {jugador.nro_jugador} - {jugador.nombre_jugador}:')
            for carta in mano:
                print(carta)
    @classmethod
    def jugador_mano_orden(cls): #hecho por jeiker
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
        return jugadores_reordenados
    
    @classmethod
    def iniciar_partida(cls):
        while cls.cuantos_jugadores() == False:
            cls.cuantos_jugadores()
        cantidad_de_jugadores = len(cls.lista_jugadores)
        palos = ('Pica', 'Corazon', 'Diamante', 'Trebol')
        nro_carta = ('A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K')
        
        mazo = Mazo()
        nro_mazos = mazo.Calcular_nro_mazos(cantidad_de_jugadores)
        for _ in range(nro_mazos):
            for palo in palos:
                for carta in nro_carta:
                    cart = Cartas(carta, palo)
                    mazo.agregar_cartas(cart)
            cart = Cartas('Joker', 'Especial')
            mazo.agregar_cartas(cart)
            # cart = Cartas('Joker', 'Especial') 
            # mazo.agregar_cartas(cart)  # no se sabe si sin 1 o 2 jokerr
            
        mazo.revolver_mazo() # mueve las cartas
        mazo.mostrar_cartas("Las cartas en el mazo son: ")
        mazo.mostrar_numero_cartas("El numero de cartas en el mazo: ")
        jugadores_reordenados = cls.jugador_mano_orden()
        manos = mazo.repartir_cartas(jugadores_reordenados)
        if mazo.cartas: # hecho por yosger -> Es necesario el if?
            cls.descarte.append(mazo.cartas.pop(-1))
        
        
        print("Inicia de Juego")
        print(f"Carta inicial en el descarte: {cls.descarte[-1]}")
        cls.mostrar_manos(jugadores_reordenados, manos)
        mazo.mostrar_cartas("Las cartas restantes en el mazo son: ")
        mazo.mostrar_numero_cartas("El numero de cartas en el mazo: ")
        cls.jugar_partida(jugadores_reordenados, manos, mazo)

    @classmethod
    def jugar_partida(cls, jugadores, manos, mazo): #Hecho por yosger
        while True:
            for i, jugador in enumerate(jugadores):
                mano_actual = manos[i] #->arreglo de cartas del jugador i
                print(f"\nEs el turno de {jugador.nombre_jugador} (Jugador {jugador.nro_jugador})") 
                print(f"Tus cartas: {[str(c) for c in mano_actual]}")
                # Esta sintaxis es igual a hacer:
                #arreglo = []
                #for c in mano_actual
                #   arreglo.append(str(c))
                #print(f"... {arreglo}")
                print(f"Carta en el descarte: {cls.descarte[-1]}")
                
                while True:
                    print("\nOpciones:")
                    print("1. Robar carta del mazo cerrado")
                    print("2. Tomar carta del descarte")
                    opcion_robar = input("Elige una opción (1 o 2): ")
                    
                    if opcion_robar == '1':
                        if mazo.cartas:
                            carta_robada = mazo.cartas.pop(-1) #->Debe ser la ultima posicion por eso "-1"
                            mano_actual.append(carta_robada)
                            print(f"Has robado: {carta_robada}")
                        else:
                            print("No hay cartas en el mazo cerrado. ¡El mazo necesita ser barajado de nuevo!")
                            continue #-> Basicamente se vuele a repetir el ciclo
                        break
                    elif opcion_robar == '2':
                        carta_descarte = cls.descarte.pop(-1)
                        mano_actual.append(carta_descarte)
                        print(f"Has tomado del descarte: {carta_descarte}")
                        break
                    else:
                        print("Opción no válida. Por favor, elige 1 o 2.")

                print("\nAhora debes descartar una carta.")
                print(f"Tus cartas actuales: {[str(c) for c in mano_actual]}")
                
                while True:
                    descarte_str = input("Ingresa la carta que quieres descartar (ej: 5 de Trebol): ")
                    
                    carta_a_descartar = None
                    for carta in mano_actual:
                        if str(carta).strip().lower() == descarte_str:
                            carta_a_descartar = carta
                            break
                    
                    if carta_a_descartar:
                        mano_actual.remove(carta_a_descartar)
                        cls.descarte.append(carta_a_descartar)
                        print(f"Has descartado: {carta_a_descartar}")
                        break
                    else:
                        print("Carta no encontrada en tu mano. Inténtalo de nuevo.")
                
                manos[i] = mano_actual
