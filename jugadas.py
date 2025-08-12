class Jugada:
    def __init__(self):
        pass
    @classmethod
    def Trio(cls,mano):
        conteo = {}
        for carta in mano:
            if(carta.numero in conteo):
                conteo[carta.numero].append(carta)
            else:
                conteo[carta.numero] = [carta]
        listas_trios = []
        for cartas in conteo.values():
            if(len(cartas) >= 3):
                listas_trios.append(cartas)
        return listas_trios
    @classmethod
    def Seguidilla(cls,mano):
        conteo = {}
        for carta in mano:
            if(carta.figura in conteo):
                conteo[carta.figura].append(carta)
            else:
                conteo[carta.figura] = [carta]
        listas_seguidilla = []
        for cartas in conteo.values():
            if(len(cartas) >= 4):
                listas_seguidilla.append(cartas)
        return listas_seguidilla
    @classmethod
    def primera_jugada(cls,mano):
        listas_trio = cls.Trio(mano)
        listas_seguidilla = cls.Seguidilla(mano)
        primera_jug = []
        if(listas_trio and listas_seguidilla):
            print("Felicidades, tienes lo requerido para la primera jugada")
            print(f"Tus trios son {list(enumerate(listas_trio))} y tus seguidillas son {list(enumerate(listas_seguidilla))}")
            nro_trio = int(input("Ingrese el numero del trio para la jugada: "))
            nro_seguidilla = int(input("Ingrese el numero de la seguidilla para la jugada: "))
            primera_jug.append(listas_trio[nro_trio])
            primera_jug.append(listas_seguidilla[nro_seguidilla])
        else:
            return False
        return primera_jug
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
Jugada.Trio()
#aun no se sabe que se hara aqui, hay que averiguarlo jajajaj
#XD