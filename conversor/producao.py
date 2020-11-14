class Producao:
    def __init__(self, id, esquerda, direita):
        self.id = id
        self.esquerda = esquerda
        self.direita = direita

    def toString(self):
        string = str(self.esquerda)+"->"

        string += ''.join(map(str, self.direita))
        
        return string