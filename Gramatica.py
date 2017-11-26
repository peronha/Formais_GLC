import types
import re

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

    # Funcao que dado um simbolo retorna o fecho deste simbolo
    def FechoTransitivoSimbolo(self, simbolo, simbolos_percorridos):

        fecho = []

        if simbolo in self.regras :
            for producao in self.regras[simbolo]:
                if producao in self.variaveis and producao != simbolo and producao not in simbolos_percorridos:
                    fecho.append(producao)
                    simbolos_percorridos.append(producao)
                    fecho_producao = self.FechoTransitivoSimbolo(producao, simbolos_percorridos)
                    for prod in fecho_producao:
                        if prod not in fecho:
                            fecho.append(prod)

        return fecho

    # Funcao que retorna o fecho transitivo de todas as variáveis da gramática
    def FechoTransitivo(self):
        fecho = {}

        for var in self.variaveis:
            simbolos_percorridos = []
            simbolos_percorridos.append(var)
            fecho[var] = self.FechoTransitivoSimbolo(var, simbolos_percorridos)


        return fecho

    # Função que retorna um array com as variáveis que possuem pelo menos uma produção vazia direta ou indiretamente.
    def ProducoesVazias(self, simbolo):
        conjuntoProducoesVazias = []
        for cabeca in self.regras:
            for producao in self.regras[cabeca]:
                if simbolo in producao:
                    conjuntoProducoesVazias.append(cabeca)
                    break

        for cabeca in self.regras:
            for producao in self.regras[cabeca]:
                for variavel in conjuntoProducoesVazias:
                    if variavel in producao and cabeca not in conjuntoProducoesVazias:
                        conjuntoProducoesVazias.append(cabeca)
                        break

        return conjuntoProducoesVazias

    # Verifica se existe uma producao de uma Variavel para um terminal
    def ExisteProducaoTerminal(self, terminal):
        for simbolo,prod in self.regras.items():
            if len(prod) == 1:
                if prod[0] == terminal:
                    return simbolo

        return None

    #dada uma produçao retorna os seus simbolos
    def SimbolosProducao(self, prod):
        simbolos = []
        matchObj = re.findall(r'[A-Z]_[a-z]|[A-Z][0-9]+|[A-Z]', prod, re.I | re.M)

        return matchObj


    def TamanhoRealProducao(self, prod):

        return 1

    # Retorna todas as variáveis que geram algum terminal
    def ProducoesTerminais(self):
        variaveis = []


        return variaveis