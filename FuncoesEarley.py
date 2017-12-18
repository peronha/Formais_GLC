from Gramatica import *
from EarlyParsingNode import *
import re

def imprimeProducoesEarley(charts):
    for indice_chart, chart in charts.items():
        for variavel, producoes in chart.items():
            for prod in producoes:
                #print(str(prod.pos_ponteiro))
                producao_string = ""
                i=0
                # Prepara a variavel da producao
                for v in prod.producao:
                    if prod.pos_ponteiro == i:
                        producao_string = producao_string + "." + str(v)
                    else:
                        producao_string = producao_string + str(v)
                    i +=1
                if len(prod.producao) == prod.pos_ponteiro:
                    producao_string = producao_string + "."

                print (str(indice_chart) + " : " + variavel + " --> " + producao_string + "\\" + str(prod.nivel) )

#Earley is not picky about what type of grammar it accepts :)
def EarleyInTheMorning(gramatica, palavra):
    #producoes iniciais partindo de S
    charts = {}
    charts[0] = converteDictEarly( produzProducoes(gramatica, 'S', 0)[0], 0, 0, gramatica)
    i = 1
    #Em algum lugar eu sujei a gramatica, entao vou purificar ela
    purificaGramatica(gramatica)
    #print(charts)
    #agora começa a parte divertida
    for c in palavra:

            charts[i] =  procuraTerminalChart(c, charts[i-1])
            if i <= len(palavra):
                producoesReduzidas(charts, i, gramatica)
                producoesProximoSimbolo(charts, i, gramatica)
                producoesReduzidas(charts, i, gramatica)
                producoesReduzidas(charts, i, gramatica)
                producoesProximoSimbolo(charts, i, gramatica)
                producoesReduzidas(charts, i, gramatica)
                producoesReduzidas(charts, i, gramatica)
                producoesProximoSimbolo(charts, i, gramatica)
                producoesReduzidas(charts, i, gramatica)
                i += 1

    imprimeProducoesEarley(charts)

    return 0

#Dada uma variavel procura em charts anteriores producoes que a geram
def procuraVarCharts(variavel_reduzida, charts, r):
    adicionar_producoes = {}
    for i in range (0, r):
        #print(charts[r])
        #Procura producoes que geram a variavel reduzida
        for idx,itens in charts[i].items():
            for e_node in itens:
                if e_node.producao[e_node.pos_ponteiro] == variavel_reduzida:
                    #instancio um novo nodo
                    novo_nodo = EarlyNode(e_node.nivel, e_node.pos_ponteiro + 1, e_node.producao)
                    if idx in adicionar_producoes:
                        adicionar_producoes[idx].append(novo_nodo)
                    else:
                        adicionar_producoes[idx] = []
                        adicionar_producoes[idx].append(novo_nodo)

        return adicionar_producoes
'''    for idx, itens in adicionar_producoes.items():
        if idx in charts[r]:
            for item in itens:
                charts[r][idx].append(item)
        else:
            charts[r][idx] = []
            for item in itens:
                charts[r][idx].append(item)'''

def producoesReduzidas(charts, r, gramatica):
    prods_add = []
    for idx, items in charts[r].items():
        for prod in items:
            if len(prod.producao) == prod.pos_ponteiro:
                variavel_reduzida = idx
                prods_add.append(procuraVarCharts(idx, charts, r))
                #procura nos charts r - 1 producoes que referenciam a variavel  reduzida
    #print(prods_add)

    for nova_producao in prods_add:
        for idx, itens in nova_producao.items():
            if idx in charts[r]:
                for item in itens:
                    charts[r][idx].append(item)
            else:
                charts[r][idx] = []
                for item in itens:
                    charts[r][idx].append(item)

def purificaGramatica(gramatica):

    for idx, item in gramatica.regras.items():
        gramatica.regras[idx] = [it for it in item if not isinstance(it, EarlyNode)]

#dado um simbolo e um chart adiciona ao chart todas producoes dele que podem gerar aquele simbolo
def producoesProximoSimbolo(charts, r, gramatica):

    lista_variaveis = []
    aumentou = 0
    #Pega todas variaveis que há ponteiros no chart atual
    for idx, items in charts[r].items():
        for item in items:
            #print(item.producao)
            if item.pos_ponteiro < len(item.producao) and  item.producao[item.pos_ponteiro] in gramatica.variaveis:
                lista_variaveis.append(item.producao[item.pos_ponteiro])

    #print(lista_variaveis)


    for variavel in lista_variaveis:
        for prod in gramatica.regras[variavel]:
            novo_nodo = EarlyNode(r, 0, prod)
            aumentou=1
            if variavel in charts[r]:
                charts[r][variavel].append(novo_nodo)
            else:
                charts[r][variavel] = []
                charts[r][variavel].append(novo_nodo)

    return aumentou
    #for c in gramatica.regras:
    #    print(c)


    #print(chart)
    #print( gramatica.regras)
    '''
    for idx, items in chart.items():
        for prod in items:
            #print(prod.producao)
            if len(prod.producao) > prod.pos_ponteiro:
                #Procura as producoes da variavel que podem gerar o proximo simbolo
                if prod.producao[prod.pos_ponteiro] in gramatica.variaveis:
                    # Percorre  as producoes da variavel pra saber se ela gera o prox_simbolo
                    for prod_v in gramatica.regras[prod.producao[prod.pos_ponteiro]]: #Kkkkkkkkkkkkkkkkk
                        #TODO Implementar
                        print("todotodotodotodo")
    '''


#return producoes
#Dado um terminal e um conjunto de producoes de Early (chart)
#retorna as producoes que incluem aquele chart
def procuraTerminalChart(terminal, chart):

    producoes = {}
    for prod, itens in chart.items():
        prods_i = []
        for item in itens:
            if len(item.producao) > item.pos_ponteiro:
                if item.producao[item.pos_ponteiro] == terminal:
                    novo_nodo = EarlyNode(item.nivel, item.pos_ponteiro + 1, item.producao )
                    prods_i.append(novo_nodo)
        if len(prods_i) > 0:
            producoes[prod] = prods_i

    return producoes
#Função que converte um dicionario na forma Producao: [ String_de_Producoes ] para Producao: [ EarlyNodes ]
def converteDictEarly(dict, pos_ponteiro, nivel, gramatica):
    for idx, item in dict.items():
        #COnverte producao a producao para um objeto Nodo de Early
        for prod in item:
            if isinstance(prod, EarlyNode):
                break #fim do laço já converteu todas as producoes do simbolo para EarlyNodes
            else:
                nodo = EarlyNode(nivel, pos_ponteiro, gramatica.SimbolosProducao(prod))
                dict[idx].append(nodo)

    #Vou percorrer de novo pra limpar a lista porque estava com preguiça de debuggar
    for idx, item in dict.items():
        dict[idx] = [it for it in item if isinstance(it, EarlyNode)]

    return dict

#Recursivamente gera todas as producoes à esquerda de uma regra :)
def verificaRegras(var, gramatica, variaveis_percorridas):
    regras = {}
    regras[var] = gramatica.regras[var]
    adicao = []
    for idx, regra in regras.items():
        for regra_i in regra:
            simbolos = gramatica.SimbolosProducao(regra_i)
            if simbolos[0] not in gramatica.terminais and simbolos[0] not in variaveis_percorridas:
                variaveis_percorridas.append(simbolos[0])
                adicao.append( verificaRegras(simbolos[0], gramatica, variaveis_percorridas) )
    #adiciona as regras adicionais às regras
    if len(adicao) > 0:
        for add in adicao:
            for idx, regra in add.items():
                #print(idx + str(regra))
                regras[idx] = regra

    return regras

def produzProducoes(gramatica, simbolo, idx):
    chart = {}
    #print(chart[0])
    variaveis_percorridas = []
    if simbolo not in gramatica.terminais:
        variaveis_percorridas.append(simbolo)
        #chart[0].append(verificaRegras(simb, gramatica))
        chart[idx] = verificaRegras(simbolo, gramatica, variaveis_percorridas)

    return chart

