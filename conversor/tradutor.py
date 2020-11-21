from gr import Gramatica 
from producao import Producao 
from transicao import Transicao

class Tradutor_Aut_para_GR:

    def __init__(self, entrada):
        self.texto_automato = open(entrada, 'r')

    #Fazer as producoes estarem em uma lista de producoes para mandar para a GR
    def traduz(self):
        alfabeto, estados, transicoes, inicial, finais = self.separa_parametros_automato()

        simbolo_inicial = 'S'

        variaveis = [simbolo_inicial, ]
        #variaveis.extend(estados)

        terminais = alfabeto

        id = 0 
        
        #Producao do símbolo inicial
        direita = [inicial, '']
        producoes = [Producao(id, simbolo_inicial, direita),]

        controle = []
        
        #Produções dos demais símbolos
        for transicao in transicoes:
            id += 1
            
            esquerda = transicao.estado
            direita = [transicao.simbolo, transicao.prox_simbolo]
            producoes.append(Producao(id, esquerda, direita))
            controle.append(transicao.estado+transicao.simbolo+transicao.prox_simbolo)
            
            #Como muitos estados são terminais e possuem transição
            #então, adiciona-se a producao em que acaba nele e não é feita transição
            if(transicao.simbolo in alfabeto and transicao.prox_simbolo in finais):
                id += 1
                producoes.append(Producao(id, transicao.estado, transicao.simbolo))
            
            if transicao.estado not in variaveis:
                variaveis.append(transicao.estado)
        
        #Cria a gramática
        
        gramatica = Gramatica(variaveis, terminais, producoes, simbolo_inicial)    

        return gramatica 

        #Separa os parâmetros da estrutura recebida
    def separa_parametros_automato(self):
        ESTADOS = 0
        ALFABETO = 1
        OUTROS = 2

        #Estrutura do automato e lista de transicoes
        automato, transicoes = self.retira_informacoes()

        #Separa cada parte da estrutur em uma lista
        automato = automato.replace('(', '')
        automato = automato.replace(')', '')
        parametros_automato = automato.split('}') 

        #Pega cada um dos parâmetros do autômato e armazena na variável correspondente

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

    #Pega a estrutura de um automato do arquivo e uma lista de transicoes
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



    