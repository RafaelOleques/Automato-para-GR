from producao import Producao 

class GR:
    def __init__(self, variaveis, terminais, producoes, simboloInicial):
        self.variaveis = variaveis
        self.terminais = terminais
        self.producoes = producoes
        self.simboloInicial = simboloInicial   

    def print(self):
        print("Símbolo inicial:")
        print(self.simboloInicial)

        print("Variaveis:")

        for variavel in self.variaveis:
            print(variavel)
            
        print("terminais:")
        for terminal in self.terminais:
            print(terminal)
        
        print("Producoes:")
        for producao in self.producoes:
            print(producao.toString())
            
