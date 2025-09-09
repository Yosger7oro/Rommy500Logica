class Cartas:
    valores = {"joker": 0, "a": 1, "j": 11, "q": 12, "k": 13}
    mazo = 54

    def __init__(self, numero, figura):
        self.numero = numero
        self.figura = figura

    def __str__(self):
        return f'{self.numero} de {self.figura}'

    def valor_numerico(self):
        
        if str(self.numero).lower() == 'joker':
            return 0
        if str(self.numero).isdigit():
            return int(self.numero)
        return Cartas.valores[str(self.numero).lower()]
