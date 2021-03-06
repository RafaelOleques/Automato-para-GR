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
            self.set_palavra( palavra)
            self.ciclos = []
            self.etapa_1()
    
    def _executa_lista(self, palavras):
        self.mostra_producoes = False
        for palavra in palavras:
            self._executa_palavra_unica(palavra)

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

        self.etapa_2(nro_ciclo+1)

    def etapa_2(self, nro_ciclo):
        #Encerra a recursão se já passou por toda a palavra
        if(nro_ciclo > self.TAMANHO_PALAVRA):
            self.etapa_3()
            if self.mostra_producoes:
                for passos in self.lista_producoes:
                    print(passos)
            return True

        terminal_atual = self.palavra[nro_ciclo-1]

        #Incializa o cliclo atual
        self.ciclos.append(Ciclo(nro_ciclo))

        #Scan
        simbolos = self.scan(nro_ciclo, terminal_atual)

        #Predict
        producoes = self.gramatica.producoes
        self.predict(producoes, nro_ciclo, simbolos)

        if(self.ciclos[nro_ciclo].getQuantidadeProducoes() == 0):
            if self.mostra_producoes:
                print(self.mensagem_erro)
            self.lista_rejeita.append(self.palavra)
            return False
        
        #Complete
        self.complete(nro_ciclo)

        self.ciclos[nro_ciclo].print(self.print)

        self.etapa_2(nro_ciclo+1)


    def etapa_3(self):        
        for eproducao in self.ciclos[self.ULTIMO_CICLO].earley_producoes:
            if eproducao.posicao_marcador == eproducao.fim and eproducao.producao.esquerda == self.gramatica.simboloInicial:
                self.lista_aceita.append(self.palavra)
                return True
        if self.mostra_producoes:
            print(self.mensagem_erro)
        
        self.lista_rejeita.append(self.palavra)
        
        return False



    def scan(self, nro_ciclo, terminal_atual):
        novos_simbolos = []

        for eproducao in self.ciclos[nro_ciclo-1].earley_producoes:
            marcador = eproducao.posicao_marcador
            if marcador >= eproducao.fim:
                continue

            posicao = eproducao.producao.direita[marcador]

            if posicao == terminal_atual:
                nova_eproducao = Earley_producao(eproducao.producao, eproducao.nro_ciclo_adicionado, eproducao.caminho)
                nova_eproducao.posicao_marcador += 1
                marcador = nova_eproducao.posicao_marcador
                
                self.ciclos[nro_ciclo].add_producao(nova_eproducao)

                if marcador != eproducao.fim:
                    novos_simbolos.append([eproducao.producao.direita[marcador], eproducao.producao.id])

        return novos_simbolos

    def predict(self, producoes, nro_ciclo, simbolos):
        analisar_prox_simbolos = False
        proximos_simbolos = []
        novas_producoes_analisar = []

        #Verifica se há variáveis dentre os símbolos recebidos
        for simbolo in simbolos:
            if simbolo[self.SIMBOLO] in self.gramatica.variaveis:
                novas_producoes_analisar.extend(self.add_ciclo(producoes, simbolo, nro_ciclo))
                analisar_prox_simbolos = True

        proximos_simbolos.extend(self.get_lista_proximo_simbolo(novas_producoes_analisar))

        #Se tiver variáveis, irá fazer um novo predidict
        if analisar_prox_simbolos:
            self.predict(producoes, nro_ciclo, proximos_simbolos)
    
    def complete(self, nro_ciclo):
        self.lista_producoes = []
        self.retorno = 0
        #Passo por todas as producoes do ciclo e vejo se alguma chegou no final
        for eproducao in self.ciclos[nro_ciclo].earley_producoes:
            if eproducao.posicao_marcador == eproducao.fim:
                
                simbolo = eproducao.producao.esquerda
                ciclo_anterior = nro_ciclo - 1
                #Verifico se consigo avancar alguma producao de um ciclo anterior
                self.avanca_producao_anterior(simbolo, nro_ciclo, ciclo_anterior)

                if self.retorno == (self.TAMANHO_PALAVRA) and nro_ciclo == self.TAMANHO_PALAVRA:
                    if eproducao.producao.esquerda != self.gramatica.simboloInicial:
                        self.lista_producoes.append(eproducao.producao.toString_sem_id())

    def avanca_producao_anterior(self, simbolo, nro_ciclo_atual, ciclo_anterior):
        #Passo pro todas as producoes do ciclo anterior
        val = 0
        for i in range(0, (ciclo_anterior+1)):
            for eproducao in self.ciclos[i].earley_producoes:
                marcador = eproducao.posicao_marcador

                if(marcador >= eproducao.fim):
                    continue
                simbolo_marcado = eproducao.producao.direita[marcador]


                if simbolo_marcado == simbolo:
                    nova_eproducao = Earley_producao(eproducao.producao, eproducao.nro_ciclo_adicionado, eproducao.caminho)
                    nova_eproducao.avanca_marcador()
                    marcador = nova_eproducao.posicao_marcador
                    
                    self.ciclos[nro_ciclo_atual].add_producao(nova_eproducao)
                    novo_simbolo = nova_eproducao.producao.esquerda
                    novo_ciclo_anterior = ciclo_anterior - 1
                    val = self.avanca_producao_anterior(novo_simbolo, nro_ciclo_atual, novo_ciclo_anterior)
                    if val is None:
                        val = 0
                    #novos_simbolos.append(eproducao.producao.direita[marcador])

                    if (eproducao.producao.esquerda == 'S' or nro_ciclo_atual == self.TAMANHO_PALAVRA):
                        self.lista_producoes.append(str(nova_eproducao.producao.toString_sem_id()))
                        self.retorno += 1
                        return 1

        
        return 0
                    

    

    #SImbolo é [string do simbolo, id do simbolo]
    def add_ciclo(self, producoes, simbolo, nro_ciclo):
        INVALIDO = ''
        novas_producoes = []

        if simbolo[self.SIMBOLO] in self.gramatica.variaveis and simbolo[self.SIMBOLO] != INVALIDO:
            for producao in producoes:
                if producao.esquerda == simbolo[self.SIMBOLO]:
                    if not self.ciclos[self.ULTIMO_CICLO].producaoJaExiste(producao):
                        novas_producoes.append(Earley_producao(producao, nro_ciclo, simbolo[self.ID]))

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



