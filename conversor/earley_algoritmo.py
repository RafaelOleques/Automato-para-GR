from ciclo import Ciclo 
from gr import Gramatica
from earley_producao import Earley_producao
from producao import Producao

class Earley:
    def __init__(self, gramatica, print=False):
        self.ciclos = []
        self.gramatica = gramatica
        self.palavra = ""
        self.retorno = 0
        self.lista_producoes = []
        self.lista_aceita = []
        self.lista_rejeita = []
        self.mostra_producoes = True

        #Constantes
        self.ULTIMO_CICLO = -1
        self.PRODUCAO = 0
        self.NRO_SIMBOLO = 1
        self.SIMBOLO = 0
        self.ID = 1

        #Mensagens
        self.print = print

    def set_palavra(self, palavra):
        self.mensagem_erro = "Palavra não pertence à linguagem"
        self.mensagem_aceita = "A palavra pertente à linguagem"
        self.TAMANHO_PALAVRA = len(palavra)
        self.palavra = palavra

    def executa(self, palavra):
        if type(palavra) is list:
            self._executa_lista(palavra)
        else:
            self._executa_palavra_unica(palavra)
            
    
    def _executa_palavra_unica(self, palavra):
            self.set_palavra(palavra)
            self.ciclos = []
            self.etapa_1()
    
    def _executa_lista(self, palavras):
        self.mostra_producoes = False

        #Aplica o algoritmo em todas as palavras recebidas
        for palavra in palavras:
            self._executa_palavra_unica(palavra)

        #Lista de aceita e rejeita
        print("\nACEITA:")
        for aceita in self.lista_aceita:
            print(aceita)

        print("\nREJEITA:")
        if self.lista_rejeita != []:
            for rejeita in self.lista_rejeita:
                print(rejeita)
        else:
            print("Nenhuma palavra foi rejeitada")
       

    def etapa_1(self):
        #Se for palavra vazia já retorna que ela não está na linguagem
        if self.palavra == '':
            if self.mostra_producoes:
                print(self.mensagem_erro)
            self.lista_rejeita.append(self.palavra)
            return False

        nro_ciclo = 0
        novas_producoes = []
        proximos_simbolos = []

        #Crio o primeiro cíclo
        self.ciclos.append(Ciclo(nro_ciclo))

        #Produções de S
        producoes = self.gramatica.producoes
        simboloInicial = self.gramatica.simboloInicial

        simbolo = [simboloInicial, None]
        
        novas_producoes.extend(self.add_ciclo(producoes, simbolo, nro_ciclo))

        #Produções a partir de S        
        proximos_simbolos = self.get_lista_proximo_simbolo(novas_producoes)

        self.predict(producoes, nro_ciclo, proximos_simbolos)

        self.ciclos[nro_ciclo].print(self.print)

        #Inicia a etapa 2
        self.etapa_2(nro_ciclo+1)

    def etapa_2(self, nro_ciclo):
        #Encerra a recursão se já passou por toda a palavra e inicia a etapa 3
        if(nro_ciclo > self.TAMANHO_PALAVRA):
            self.etapa_3()

            #Depois que termina a etapa 3 (só chega aqui se a palavra está na linguagem) 
            #Mostra a produção (palavra única) / retorna verdadeiro (lista de palavras)
            if self.mostra_producoes:
                for passos in self.lista_producoes:
                    print(passos)
            return True

        #Início da etapa 2

        #Terminal que está sendo identificado na palavra nesse passo
        terminal_atual = self.palavra[nro_ciclo-1]

        #Incializa o cliclo atual
        self.ciclos.append(Ciclo(nro_ciclo))

        #Scan
        simbolos = self.scan(nro_ciclo, terminal_atual)

        #Predict
        producoes = self.gramatica.producoes
        self.predict(producoes, nro_ciclo, simbolos)

        #Se o ciclo tem 0 produções, então a palavra não está nele e sai da recursão
        #Mostrando a mensagem de rejeita (palavra única) / Adicionando na lista de rejeita (lista de palavras) 
        if(self.ciclos[nro_ciclo].getQuantidadeProducoes() == 0):
            if self.mostra_producoes:
                print(self.mensagem_erro)
            self.lista_rejeita.append(self.palavra)
            return False
        
        #Complete
        self.complete(nro_ciclo)

        self.ciclos[nro_ciclo].print(self.print)

        #Recursão para o próximo símbolo
        self.etapa_2(nro_ciclo+1)


    def etapa_3(self):   
        #Passa por todas as palavras do último ciclo     
        for eproducao in self.ciclos[self.ULTIMO_CICLO].earley_producoes:
            #Se o tiver a produção do símbolo inicial e o marcador estiver no fim
            #Adiciona a palavra na lista de aceita / Retorna verdadeiro 
            if eproducao.posicao_marcador == eproducao.fim and eproducao.producao.esquerda == self.gramatica.simboloInicial:
                self.lista_aceita.append(self.palavra)
                return True
        
        #Se não for o anterior, mostrar a mensagem que não pertence a linguagem (palavra única)
        if self.mostra_producoes:
            print(self.mensagem_erro)
        
        #Adiciona na lista de rejeita (lista de palavras) e retorna falso
        self.lista_rejeita.append(self.palavra)
        
        return False


    def scan(self, nro_ciclo, terminal_atual):
        novos_simbolos = []

        #Passa pelas produções do ciclo anterior e vê onde está o marcador
        for eproducao in self.ciclos[nro_ciclo-1].earley_producoes:
            marcador = eproducao.posicao_marcador
            #Se o marcador já estiver no final, não faz nada nela
            if marcador >= eproducao.fim:
                continue

            #Pega o símbolo que está o marcador
            posicao = eproducao.producao.direita[marcador]

            #Se a o símbolo for o terminal sendo analisado
            if posicao == terminal_atual:
                #Cria uma cópia da produção
                nova_eproducao = Earley_producao(eproducao.producao, eproducao.nro_ciclo_adicionado, eproducao.caminho)
                #Avança o marcador
                nova_eproducao.posicao_marcador += 1
                marcador = nova_eproducao.posicao_marcador
                
                #Adiciona a produção no ciclo
                self.ciclos[nro_ciclo].add_producao(nova_eproducao)

                #Se o marcador já não passou do final da produção, adiciona para os próximos símbolos para predict
                if marcador != eproducao.fim:
                    novos_simbolos.append([eproducao.producao.direita[marcador], eproducao.producao.id])

        return novos_simbolos

    def predict(self, producoes, nro_ciclo, simbolos):
        analisar_prox_simbolos = False
        proximos_simbolos = []
        novas_producoes_analisar = []

        #Verifica se há variáveis dentre os símbolos recebidos
        for simbolo in simbolos:
            #Se for variável
            if simbolo[self.SIMBOLO] in self.gramatica.variaveis:
                #Adiciona para as produções que vão para o predict
                #Adiciona no cíclo
                novas_producoes_analisar.extend(self.add_ciclo(producoes, simbolo, nro_ciclo))
                analisar_prox_simbolos = True

        #Pega os símbolos aplicados para o predict
        proximos_simbolos.extend(self.get_lista_proximo_simbolo(novas_producoes_analisar))

        #Se tiver variáveis, irá fazer um novo predidict
        if analisar_prox_simbolos:
            self.predict(producoes, nro_ciclo, proximos_simbolos)

        #SImbolo é [string do simbolo, id do simbolo]
    def add_ciclo(self, producoes, simbolo, nro_ciclo):
        INVALIDO = ''
        novas_producoes = []

        #Verifico se o símbolo é uma variável e se é válido
        if simbolo[self.SIMBOLO] in self.gramatica.variaveis and simbolo[self.SIMBOLO] != INVALIDO:
            for producao in producoes:
                #Se o símbolo é a esquerda de uma produção
                if producao.esquerda == simbolo[self.SIMBOLO]:
                    #E já não está dentro do meu ciclo
                    if not self.ciclos[self.ULTIMO_CICLO].producaoJaExiste(producao):
                        #Adiciono na minha lista de produções para o predict
                        novas_producoes.append(Earley_producao(producao, nro_ciclo, simbolo[self.ID]))

        #Também adiciono no meu ciclo
        for eproducao in novas_producoes:
            self.ciclos[self.ULTIMO_CICLO].add_producao(eproducao)


        return novas_producoes

    #Lista do proximo simbolo para o predict
    #Se pega somente o primeiro, uma vez que se quer as producoes mais a esquerda
    def get_lista_proximo_simbolo(self, eproducoes):
        lista_prox = []
        PRIMEIRO_SIMBOLO = 0

        for eproducao in eproducoes:
            lista_prox.append([eproducao.producao.direita[PRIMEIRO_SIMBOLO], eproducao.producao.id])
        
        return lista_prox
    
    def complete(self, nro_ciclo):
        self.lista_producoes = []
        self.retorno = 0
        #Passa por todas as producoes do ciclo e vejo se alguma chegou no final
        for eproducao in self.ciclos[nro_ciclo].earley_producoes:
            if eproducao.posicao_marcador == eproducao.fim:
                
                #Vejo qual é o estado que chegou em uma final
                simbolo = eproducao.producao.esquerda
                #Pega o ciclo anterior para começar o complete
                ciclo_anterior = nro_ciclo - 1
                #Verifico se consigo avancar alguma producao de um ciclo anterior com a variável do estado final
                self.avanca_producao_anterior(simbolo, nro_ciclo, ciclo_anterior)

                #Se conseguiu uma produção que indo dela da complete em todos os estados chegando no inicial
                if self.retorno == (self.TAMANHO_PALAVRA) and nro_ciclo == self.TAMANHO_PALAVRA:
                    #Se ela não for o próprio inicial
                    if eproducao.producao.esquerda != self.gramatica.simboloInicial:
                        #Adiciona na lista de produções para mostrar no final
                        #Essa lista foi completada recursivamente pelo método avanca_producao_anterior
                        self.lista_producoes.append(eproducao.producao.toString_sem_id())

    #Passo por todas as producoes dos ciclos anterior ao atual recursivamente
    def avanca_producao_anterior(self, simbolo, nro_ciclo_atual, ciclo_anterior):
        #Passo por todos os ciclos anteriores ao que estou analisando
        for i in range(0, (ciclo_anterior+1)):
            #Passo por todas as produções do ciclo
            for eproducao in self.ciclos[i].earley_producoes:
                marcador = eproducao.posicao_marcador

                #Se a produção já foi completada, pulo ela
                if(marcador >= eproducao.fim):
                    continue

                #Vejo o símbolo que está marcado na produção
                simbolo_marcado = eproducao.producao.direita[marcador]

                #Se o símbolo marcado é o que foi dado complete
                if simbolo_marcado == simbolo:
                    #Faço uma cópia da produção
                    nova_eproducao = Earley_producao(eproducao.producao, eproducao.nro_ciclo_adicionado, eproducao.caminho)
                    #Avanço o marcador da cópia
                    nova_eproducao.avanca_marcador()
                    #Salvo a posição marcada
                    marcador = nova_eproducao.posicao_marcador
                    
                    #Adiciono a cópia no meu ciclo atual
                    self.ciclos[nro_ciclo_atual].add_producao(nova_eproducao)

                    #Como sei que pelo algortimo de tradução do AFD para GR sempre que avanço uma variável,
                    #então dou complete nela e, então, verifico se ela pode dar complete em alguma produção do ciclo anteio 
                    novo_simbolo = nova_eproducao.producao.esquerda
                    #Estabelo que o ciclo a ser analisado é somente os anteriores ao que houve complete
                    novo_ciclo_anterior = ciclo_anterior - 1
                    #Chamo recursivamente
                    self.avanca_producao_anterior(novo_simbolo, nro_ciclo_atual, novo_ciclo_anterior)

                    #Se eu cheguei na posição inicial e estou no ciclo de mesmo tamanho que a palavra
                    #então sei que posso acabar a recursão e que possivelmente consegui encontrar um caminho
                    if (eproducao.producao.esquerda == 'S' and nro_ciclo_atual == self.TAMANHO_PALAVRA):
                        self.lista_producoes.append(str(nova_eproducao.producao.toString_sem_id()))
                        self.retorno += 1
                        return True

        #Encerra a recursão
        return False
    



