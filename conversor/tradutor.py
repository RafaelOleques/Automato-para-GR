from gr import GR 
from producao import Producao 
from transicao import Transicao

class Tradutor_Aut_para_GR:

    def __init__(self, entrada):
        self.texto_automato = open(entrada, 'r')

    def retira_informacoes(self):
        
        AUTOMATO = 0
        TRANSICOES_INIC = 2
        num_linha = 0
        transicoes = []

        for linha in self.texto_automato:
            if num_linha == AUTOMATO:
                posicao_inicial = linha.index('=') + 1
                automato = linha[posicao_inicial:]
                
            elif num_linha >= TRANSICOES_INIC:
                transicao = Transicao(linha.replace('\n', ''))
                transicoes.append(transicao)

            num_linha += 1

        return automato, transicoes

    def separa_parametros_automato(self):
        ESTADOS = 0
        ALFABETO = 1
        OUTROS = 2

        automato, transicoes = self.retira_informacoes()

        automato = automato.replace('(', '')
        automato = automato.replace(')', '')
        parametros_automato = automato.split('}') 

        estados = parametros_automato[ESTADOS].replace('{', '')
        estados = estados.split(',')

        alfabeto = parametros_automato[ALFABETO].replace('{', '')
        alfabeto = alfabeto.split(',')
        alfabeto.remove('')

        outros = parametros_automato[OUTROS].replace('Prog', '')
        outros = outros.split('{')

        inicial = outros[0].replace(',', '')

        finais = outros[1]
        finais = finais.split(',')

        return alfabeto, estados, transicoes, inicial, finais

    #Fazer as producoes estarem em uma lista de producoes para mandar para a GR

    def traduz(self):
        alfabeto, estados, transicoes, inicial, finais = self.separa_parametros_automato()

        simbolo_inicial = 'S'

        variaveis = ['S', ]
        variaveis.extend(estados)

        terminais = alfabeto

        id = 0 
        
        producoes = [Producao(id, simbolo_inicial, inicial),]

        for transicao in transicoes:
            id += 1

            direita = [transicao.simbolo, transicao.prox_simbolo]
            producoes.append(Producao(id, transicao.estado, direita))

        gramatica = GR(variaveis, terminais, producoes, simbolo_inicial)    

        return gramatica 
    