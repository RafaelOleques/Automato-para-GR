from ciclo import Ciclo 
from gr import GR
from earley_producao import Earley_producao
from producao import Producao

class Earley:
    def __init__(self, gramatica, palavra):
        self.ciclos = []
        self.gramatica = gramatica
        self.palavra = palavra

    def etapa_1(self):
        nro_ciclo = 0
        ciclo0 = Ciclo(nro_ciclo)

        #Produções de S
        producoes = self.gramatica.producoes
        simboloInicial = self.gramatica.simboloInicial

        #Scan
        for producao in producoes:
            if producao.esquerda == simboloInicial:
                ciclo0.add_producao(producao, nro_ciclo)
        
        ciclo0.print()

        return ciclo0