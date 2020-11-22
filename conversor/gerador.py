from tradutor import Tradutor_Aut_para_GR
from gr import Gramatica
from early_algoritmo import Earley

class Gerador:
    def __init__(self):

        automato = input("Digite o caminho para o automato: ")

        tipo = input("Para a entrada: 0 para arquivo / 1 para texto: ")
        informacao = input("Digite a entrada: ")

        entrada = (tipo, informacao)

        palavras = self.trata_entrada(entrada)

        tradutor = Tradutor_Aut_para_GR(automato)
        gramatica = tradutor.traduz()

        if gramatica == False:
            print("Entrada inválida!")

        #gramatica.print()

        for palavra in palavras:
            earley = Earley(gramatica, entrada, print=True)
            earley.executa()

    def trata_entrada(self, entrada):
        TIPO = 0
        INFORMACAO = 1
        ARQUIVO = 0

        lista_palavras = []

        if(entrada[TIPO] == ARQUIVO):
            #tratamento
            pass
        else:
            return [entrada[INFORMACAO],]

if __name__ == "__main__":   
    #entrada = './Automato_Entrada.txt'
    gerador = Gerador()
