from earley_producao import Earley_producao 
from producao import Producao

class Ciclo:
    def __init__(self, nro_ciclo):
        self.earley_producoes = []
        self.nro_ciclo = nro_ciclo

    def add_producao(self, producao, nro_ciclo):
        self.earley_producoes.append(Earley_producao(producao, nro_ciclo))

    def getProducoes(self):
        return self.earley_producoes

    def getMarcados(self):
        marcados = []

        for eproducao in self.earley_producoes:
            marcados.append(eproducao.producao.marcado())

        return marcados

    def print(self):
        print("Ciclo atual:", self.nro_ciclo)

        print("Produções: ")
        for eproducoes in self.earley_producoes:
            print(eproducoes.toString())
