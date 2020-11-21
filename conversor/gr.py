from producao import Producao 

class Gramatica:
    def __init__(self, variaveis, terminais, producoes, simboloInicial):
        self.variaveis = variaveis
        self.terminais = terminais
        self.producoes = producoes
        self.simboloInicial = simboloInicial 

        #self.atualiza_producoes()

    #Retira das producoes as variaveis que não possuem transicao
    '''
    def atualiza_producoes(self):
        for producao in self.producoes:
            producoes_direita = []
            producoes_direita.extend(producao.direita)

            for direita in producoes_direita:
                if direita not in self.variaveis and direita not in self.terminais:
                    producao.direita.remove(direita)
    '''

    def print(self):
        print("Símbolo inicial:")
        print(self.simboloInicial)

        print("Variaveis:")
        print(self.variaveis)

        #for variavel in self.variaveis:
            #print(variavel)
            
        print("terminais:")
        print(self.terminais)
        #for terminal in self.terminais:
            #print(terminal)
        
        print("Producoes:")
        for producao in self.producoes:
            print(producao.toString())
            
