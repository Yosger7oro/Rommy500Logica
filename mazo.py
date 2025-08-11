from random import sample, shuffle
class Mazo:
    def __init__(self):
        self.cartas = []
        self.cartas_finales = []
    
    def agregar_cartas(self,carta):
        self.cartas.append(carta)
    def Calcular_nro_mazos(self,numero_de_jugadores):
        resultado = numero_de_jugadores // 3  
        if numero_de_jugadores % 3 != 0:
            resultado += 1
        return resultado
    def revolver_mazo(self):
        shuffle(self.cartas)

    def mostrar_cartas(self):
        print('Cartas en el mazo:')
        for carta in self.cartas:
            print(carta)


    def mostrar_numero_cartas(self):
        print(f'El numero de cartas es {len(self.cartas)}')

    def mostrar_nuevas_cartas(self):
        print(f'Cartas restantes en el mazo: ')
        for carta in self.cartas_finales:
            print(carta)
    def repartir_cartas(self,lista_de_jugadores):
        num_jugadores = len(lista_de_jugadores)
        cartas_indice_repartidas = sample(list(enumerate(self.cartas)), 10*num_jugadores)
        cartas_repartidas = []
        indice_de_cartas_eliminar = []
        for x in cartas_indice_repartidas:
            cartas_repartidas.append(x[1])
            indice_de_cartas_eliminar.append(x[0])

        jugadores = []
        for _ in range(num_jugadores):
            jugadores.append([])
        for index,carta in enumerate(cartas_repartidas):
            indice_de_jugador = index % num_jugadores
            jugadores[indice_de_jugador].append(carta)
        self.cartas_finales = self.cartas[:] #Esta sintaxis permite guardar el valor de self.carta como una copia, sin esto dos puntos al modificar cartas_finales modificarian cartas
        for indice in sorted(indice_de_cartas_eliminar,reverse=True):
            self.cartas_finales.pop(indice)
        return jugadores

        # for i,mano in enumerate(jugadores):
        #     jugador = lista_de_jugadores[i]
        #     print(f'Cartas del jugador {jugador.nro_jugador} - {jugador.nombre_jugador}: ')
        #     for x in mano:
        #         print(f'{x.numero} de {x.figura}')