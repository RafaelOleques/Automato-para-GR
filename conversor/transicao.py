class Transicao:
    def __init__(self, texto):   
        ESTADO = 0
        SIMBOLO = 1
        PROX = 2

        texto = texto.replace('(', '')
        texto = texto.replace(')', '')
        texto = texto.replace('=', ',')

        forma_transicao = texto.split(',')

        self.estado = forma_transicao[ESTADO]
        self.simbolo = forma_transicao[SIMBOLO]
        self.prox_simbolo = forma_transicao[PROX]

    
