from tradutor import Tradutor_Aut_para_GR
from gr import Gramatica
from early_algoritmo import Earley

class Gerador:
    def __init__(self, entrada, palavra):
        tradutor = Tradutor_Aut_para_GR(entrada)
        gramatica = tradutor.traduz()
        #gramatica.print()
        earley = Earley(gramatica, palavra, print=True)
        earley.executa()

if __name__ == "__main__":   
    entrada = './Automato_Entrada.txt'
    gerador = Gerador(entrada, 'MMCXVIII')
