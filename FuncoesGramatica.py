from Gramatica import *
import re

def carregaGramatica(nomeArq):

    gramatica = Gramatica()

    escreve_terminais = 0
    escreve_variaveis = 0
    escreve_regras = 0
    escreve_inicial = 0

    with open(nomeArq) as arq:
        for dado in arq:

            matchT = re.match(r'#Terminais',dado, re.I|re.M)
            if matchT:
                escreve_terminais = 1
                escreve_regras = 0
                escreve_variaveis = 0
                escreve_inicial = 0
            matchV = re.match(r'#Variaveis',dado, re.I|re.M)
            if matchV:
                escreve_terminais = 0
                escreve_regras = 0
                escreve_variaveis = 1
                escreve_inicial = 0
            matchR = re.match(r'#Regras', dado, re.I|re.M)
            if matchR:
                escreve_terminais =0
                escreve_regras=1
                escreve_variaveis=0
                escreve_inicial = 0
            matchI = re.match(r'#Inicial', dado, re.I|re.M)
            if matchI:
                escreve_terminais =0
                escreve_regras=0
                escreve_variaveis=0
                escreve_inicial = 1

            if escreve_terminais :
               matchObj  = re.match(r'\[ (\w) \]', dado, re.I|re.M)
               if matchObj:
                gramatica.adicionaTerminais(matchObj.group(1))

            if escreve_variaveis :
                matchObj = re.match(r'\[ (\w) \]', dado, re.I | re.M)
                if matchObj:
                    gramatica.adicionaVariavel(matchObj.group(1))

            if escreve_regras :
                matchObj = re.findall(r'\[ (\w) \]', dado, re.I | re.M)
                if matchObj:
                    gramatica.adicionaRegra(matchObj[0], "".join(matchObj[1:]))

            if escreve_inicial :
                matchObj = re.match(r'\[ (\w) \]', dado, re.I | re.M)
                if matchObj:
                    gramatica.defineInicial(matchObj.group(1))


            #print(dado)

    return gramatica