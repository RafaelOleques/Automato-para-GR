from producao import Producao 

class Earley_producao:
    def __init__(self, producao, nro_ciclo_adicionado):
        self.producao = producao
        self.posicao_marcador = 0
        self.nro_ciclo_adicionado = nro_ciclo_adicionado

    def avanca_marcador(self):
        self.posicao_marcador += 1

    def marcado(self):
        return self.producao.direita[self.posicao_marcador]

    def toString(self):
        string =  "(Ciclo: "+str(self.nro_ciclo_adicionado)+"), "
        string += "(Marcador: "+str(self.posicao_marcador)+"), "
        string += "("+self.producao.toString()+")\n"

        return string