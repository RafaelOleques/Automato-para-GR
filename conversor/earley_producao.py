from producao import Producao 

class Earley_producao:
    def __init__(self, producao, nro_ciclo_adicionado, caminho):
        self.producao = producao
        self.posicao_marcador = 0
        self.fim = self.calcula_fim()

        self.nro_ciclo_adicionado = nro_ciclo_adicionado
        self.caminho = caminho

    def calcula_fim(self):
        INVALIDO = ''
        ultimo = self.producao.direita[-1]

        if ultimo == INVALIDO:
            return len(self.producao.direita) -1
        else:
            return len(self.producao.direita)


    def avanca_marcador(self):
        self.posicao_marcador += 1

    #Poisção onde está o marcador
    def marcado(self):
        return self.producao.direita[self.posicao_marcador]

    def comparaProducoes(self, producao_verificar):
        if self.producao.id == producao_verificar.id:
            if self.producao.esquerda == producao_verificar.esquerda:
                if self.producao.direita == producao_verificar.direita:
                    return True
        
        return False

    def toString(self):
        string =  "(Ciclo: "+str(self.nro_ciclo_adicionado)+"), "
        string += "(Marcador: "+str(self.posicao_marcador)+"), "
        string += "("+self.producao.toString()+"), "
        string += "(Caminho: %s)" % self.caminho
        string += ", |Tamanho: " + str(self.fim)

        return string

    