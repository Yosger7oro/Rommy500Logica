class Jugador:
    def __init__(self, nro, nombre):
        self.nro_jugador = nro
        self.nombre_jugador = nombre
        self.primera_jugada_hecha = False

# necesitamos ver si usar el __str__ aqui o no -> podria ser de ayuda, retorna la cadena de texto y asi en otras partes no lo llamamos como objeto