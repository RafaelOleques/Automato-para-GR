from ciclo import Ciclo 
from gr import GR
from earley_producao import Earley_producao
from producao import Producao

class Earley:
    def __init__(self, gramatica, palavra):
        self.ciclos = []
        self.gramatica = gramatica
        self.palavra = palavra

    def get_lista_proximo_simbolo(self, producoes):
        lista_prox = []

        for producao in producoes:
            lista_prox.append(producao[0].direita[0])
        
        return lista_prox

    def add_ciclo(self, producoes, simbolo, nro_ciclo):
        novas_producoes = []
        i = 0
        if simbolo in self.gramatica.variaveis and simbolo != '':
            for producao in producoes:
                if producao.esquerda == simbolo:
                    if not self.ciclos[-1].producaoJaExiste(producao):
                        novas_producoes.append((producao, nro_ciclo))

        for producao in novas_producoes:
            self.ciclos[-1].add_producao(producao[0], producao[1])

        return novas_producoes

    def predict(self, producoes, nro_ciclo, simbolos):
        analisar_prox_simbolos = False
        proximos_simbolos = []
        novas_producoes_analisar = []

        for simbolo in simbolos:
            if simbolo in self.gramatica.variaveis:
                novas_producoes_analisar.extend(self.add_ciclo(producoes, simbolo, nro_ciclo))
                analisar_prox_simbolos = True

        proximos_simbolos.extend(self.get_lista_proximo_simbolo(novas_producoes_analisar))
        
        if analisar_prox_simbolos:
            self.predict(producoes, nro_ciclo, proximos_simbolos)

    def etapa_1(self):
        nro_ciclo = 0
        novas_producoes = []
        proximos_simbolos = []

        self.ciclos.append(Ciclo(nro_ciclo))

        #Produções de S
        producoes = self.gramatica.producoes
        simboloInicial = self.gramatica.simboloInicial

        novas_producoes.extend(self.add_ciclo(producoes, simboloInicial, nro_ciclo))
        
        #Produções a partir de S        
        proximos_simbolos = self.get_lista_proximo_simbolo(novas_producoes)

        self.predict(producoes, 0, proximos_simbolos)
        
        self.ciclos[0].print()

    def etapa_2(self):
        pass

    def etapa_3(self):
        pass
