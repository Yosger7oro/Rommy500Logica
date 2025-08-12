class Cartas:
    mazo = 54 # esto es necesario? -> no realmente
    def __init__(self, numero, figura):
        self.numero = numero
        self.figura = figura

    def __str__(self):
        return f'{self.numero} de {self.figura}'
    
#soy tomas jajajajaj