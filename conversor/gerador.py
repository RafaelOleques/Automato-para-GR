from tradutor import Tradutor_Aut_para_GR
from gr import Gramatica
from earley_algoritmo import Earley
from tratamento_entrada import Tratamento_entrada

class Gerador:
    def __init__(self):

        automato = input("Digite o caminho para o automato: ")

        entrada = input("Digite a entrada ou o caminho para um csv: ")

        tradutor = Tradutor_Aut_para_GR(automato)
        gramatica = tradutor.traduz()

        if gramatica is None:
            print("Autômato inválido!")
            return None

        verificador = Earley(gramatica, print=False)

        tratamento = Tratamento_entrada(entrada)
        lista_palavras = tratamento.get_entrada()

        if lista_palavras is None:
            print("CSV inválido")
            return None

        verificador.executa(lista_palavras)

if __name__ == "__main__":   
    gerador = Gerador()
