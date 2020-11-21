from earley_producao import Earley_producao 
from producao import Producao

class Ciclo:
    def __init__(self, nro_ciclo):
        self.earley_producoes = []
        self.nro_ciclo = nro_ciclo

    def add_producao(self, earley_producao):
        self.earley_producoes.append(earley_producao)

    def getProducoes(self):
        return self.earley_producoes

    def getQuantidadeProducoes(self):
        return len(self.earley_producoes)

    def getMarcados(self):
        marcados = []

        for eproducao in self.earley_producoes:
            marcados.append(eproducao.producao.marcado())

        return marcados

    def producaoJaExiste(self, producao_verificar):
        if self.earley_producoes == []:
            return False
        
        verificacao = True
        for eproducao in self.earley_producoes:
            verificacao = verificacao and eproducao.comparaProducoes(producao_verificar)

        return verificacao


    def print(self, mostra=False):
        if mostra:
            print("-----------------------------")
            print("Ciclo atual:", self.nro_ciclo)
            print("_____________________________")

            for eproducoes in self.earley_producoes:
                print(eproducoes.toString())