import csv


class Tratamento_entrada:
    def __init__(self, entrada, tipo=None):
        self.entrada = self.set_arquivo(entrada, tipo)

    def get_entrada(self):
        return self.entrada

    def set_arquivo(self, entrada, tipo):
        if ".txt" in entrada and tipo == "txt":
            return self.leitura_txt(entrada)
        elif ".csv" in entrada and (tipo == "csv" or tipo is None):
            return self.leitura_csv(entrada)
        elif tipo is not None:
            return None
        else:
            return entrada

    def leitura_txt(self, entrada):
        try:
            return open(entrada, 'r')
        except:
            return None

    def leitura_csv(self, entrada):
        try:
            with open(entrada, 'r') as arquivo_csv:
                leitor = csv.reader(arquivo_csv, delimiter='\n')

                lista_palavras = []

                for palavras in leitor:
                    for palavra in palavras:
                        lista_palavras.append(palavra)
                        
                return lista_palavras
        except:
            return None

