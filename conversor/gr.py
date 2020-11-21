from producao import Producao 

class Gramatica:
    def __init__(self, variaveis, terminais, producoes, simboloInicial):
        self.variaveis = variaveis
        self.terminais = terminais
        self.producoes = producoes
        self.simboloInicial = simboloInicial 

    def print(self):
        print("Símbolo inicial:")
        print(self.simboloInicial)

        print("Variaveis:")
        print(self.variaveis)
        
        print("terminais:")
        print(self.terminais)
        
        print("Producoes:")
        for producao in self.producoes:
            print(producao.toString())
            
