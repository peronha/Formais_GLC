import types

class Gramatica:

    def __init__(self):
        self.regras = {}
        self.terminais = []
        self.variaveis = []
        self.inicial = None

    def adicionaVariavel(self, vari):
        self.variaveis.append(vari)

    def adicionaTerminais(self, ter):
        self.terminais.append(ter)

    def adicionaRegra(self, vari, result):
        if not vari in self.regras:
            self.regras[vari] = []

        if type(result) is list:
            for c in result:
                self.regras[vari].append(c)
        else:
            self.regras[vari].append(result)

    def defineInicial(self, inicial):
        self.inicial = inicial


    def mostraGramatica(self):
        print("TERMINAIS: ")
        print(self.terminais)
        print("VARIAVEIS: ")
        print(self.variaveis)
        print("INICIAL: ")
        print(self.inicial)
        print("REGRAS: ")
        print(self.regras)