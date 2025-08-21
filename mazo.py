from random import sample, shuffle
class Mazo:
    def __init__(self):
        self.cartas = []
    def agregar_cartas(self,carta):
        self.cartas.append(carta)
    def calcular_nro_mazos(self,numero_de_jugadores):
        resultado = numero_de_jugadores // 3  
        if numero_de_jugadores % 3 != 0:
            resultado += 1
        return resultado
    def revolver_mazo(self):
        shuffle(self.cartas)

    def mostrar_cartas(self,mensaje):
        print(mensaje)
        for carta in self.cartas:
            print(carta)
    def mostrar_numero_cartas(self,mensaje):
        print(str(mensaje) + str(len(self.cartas)))

    def repartir_cartas(self,lista_de_jugadores):
        num_jugadores = len(lista_de_jugadores)
        cartas_indice_repartidas = sample(list(enumerate(self.cartas)), 10*num_jugadores)
        cartas_repartidas = [] #Cartas a repartir
        indice_de_cartas_eliminar = [] #Indice de cartas a eliminar
        for x in cartas_indice_repartidas:
            cartas_repartidas.append(x[1])
            indice_de_cartas_eliminar.append(x[0])
        jugadores = [] #lista que guardara una lista con cartas para cada jugadores [[],[],..]
        for _ in range(num_jugadores):
            jugadores.append([])
        for index, carta in enumerate(cartas_repartidas):
            indice_de_jugador = index % num_jugadores
            jugadores[indice_de_jugador].append(carta)

        for indice in sorted(indice_de_cartas_eliminar,reverse=True):
            self.cartas.pop(indice)
        
        #El sorted(lista) -> Se encarga de ordenar en forma ascendente por defecto, sin embargo el reverse="True" hace que se ordene en forma descendente, ademas el sorted(lista) no modifica la lista, el literalmente crea otra lista. El ciclo de antes funciona asi: al aplicar el sorted al indice_de_cartas_eliminar, por ejemplo. indice_de_cartas_eliminar = [1,2,5,9,3] el sorted lo deja, [9,5,3,2,1] entonces el ciclo en su primer valor tomara 9, se borra de las cartas, la carta que estaba en la posicion 9. 
        
        return jugadores
