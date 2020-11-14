from tradutor import Tradutor_Aut_para_GR
from gr import GR
from early_algoritmo import Earley

class Gerador:
    def __init__(self, entrada, palavra):
        tradutor = Tradutor_Aut_para_GR(entrada)
        gramatica = tradutor.traduz()
        gramatica.print()

        print("-------------")

        earley = Earley(gramatica, palavra)
        earley.etapa_1()

if __name__ == "__main__":   
    entrada = './Automato_Entrada.txt'
    gerador = Gerador(entrada, 'IV')
