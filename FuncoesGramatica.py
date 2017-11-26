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
                gramatica.adicionaTerminais(matchObj.group(1).strip())

            if escreve_variaveis :
                matchObj = re.match(r'\[ (\w) \]', dado, re.I | re.M)
                if matchObj:
                    gramatica.adicionaVariavel(matchObj.group(1).strip())

            if escreve_regras :
                matchObj = re.findall(r'\[ (\w) \]', dado, re.I | re.M)
                if matchObj:
                    gramatica.adicionaRegra(matchObj[0], "".join(matchObj[1:]).strip())

            if escreve_inicial :
                matchObj = re.match(r'\[ (\w) \]', dado, re.I | re.M)
                if matchObj:
                    gramatica.defineInicial(matchObj.group(1).strip())


            #print(dado)

    return gramatica


def RemoveProducoesVazias(gramatica):

    # Gera conjunto das variáveis que produzem direta ou indiretamente a palavra vazia.
    conjuntoProducoesVazias = gramatica.ProducoesVazias('V')

    # Impressão das regras na tela antes de qualquer mudança.
    #print(gramatica.regras)

    # Exclui as produções vazias (diretas).
    for cabeca in gramatica.regras:
        for producao in gramatica.regras[cabeca]:
            if 'V' in producao:
                gramatica.regras[cabeca].remove(producao)
                break

    # Gera produções adicionais sem variáveis que produzem a palavra vazia.
    # AINDA FALTA TRATAR OS CASOS DO TIPO EM QUE "ASA" GERA NOVAS PRODUÇÕES "SA", "AS" e "S".
    # Com a implementação atual "ASA" está gerando somente produções "S".
    novasProducoes = {}
    for cabeca in gramatica.regras:
        novasProducoes[cabeca] = []
        for producao in gramatica.regras[cabeca]:
            for variavel in conjuntoProducoesVazias:
                if variavel in producao and len(producao) > 1:
                    novasProducoes[cabeca].append(producao.replace(variavel, ''))
    for cabeca in gramatica.regras:
        if cabeca in novasProducoes and len(novasProducoes[cabeca]) > 0:
            for novaProducao in novasProducoes[cabeca]:
                gramatica.regras[cabeca].append(novaProducao)

    #print(gramatica.regras)

    return gramatica

# Remove todas as produções do Tipo A -> V
def RemoveProducoesUnitarias(gramatica):

    fecho_transitivo = gramatica.FechoTransitivo()
    #print(gramatica.variaveis)

    # exclui as producoes de simbolos
    for simbolo,producoes in gramatica.regras.items():
        for prod in producoes[:]:
            if prod in gramatica.variaveis:
                gramatica.regras[simbolo].remove(prod)

    # Inclui as producoes do Fecho Transitivo nas variaveis da gramatica
    for  simb,prod  in fecho_transitivo.items():
        if len(prod) > 0:
            for v in prod:
                for v_prod in gramatica.regras[v]:
                    if v_prod not in gramatica.regras[simb]:
                        gramatica.regras[simb].append(v_prod)

    return gramatica


# Remove os símbolos não atingíveis e símbolos não geradores.
def RemoveSimbolosInuteis(gramatica):

    # Remoção dos símbolos não geradores.
    for simbolo in gramatica.variaveis:
        if simbolo in gramatica.regras:
            if len(gramatica.regras[simbolo]) == 0:
                del gramatica.regras[simbolo]

    # Indica o status utilizando 0 para "Não atingível" ou 1 para "Atingível".
    simbolosStatus = {}

    # Busca quais são os símbolos não atingíveis.
    for simbolo in gramatica.variaveis:
        simbolosStatus[simbolo] = 0
        for cabeca in gramatica.regras:
            for producao in gramatica.regras[cabeca]:
                if simbolo in producao:
                    simbolosStatus[simbolo] = 1
                if simbolosStatus[simbolo] == 1:
                    break
            if simbolosStatus[simbolo] == 1:
                break

    # Remove os símbolos não atingíveis, com exceção do inicial.
    for simbolo in simbolosStatus:
        if simbolo in gramatica.regras and simbolo != gramatica.inicial and simbolosStatus[simbolo] == 0:
            del gramatica.regras[simbolo]

    return gramatica


def FormaNormalChomsky(gramatica):
    gramatica = RemoveProducoesVazias(gramatica)
    gramatica = RemoveProducoesUnitarias(gramatica)
    gramatica = RemoveSimbolosInuteis(gramatica)

    # Lista das novas variaveis que geram apenas um terminal no formato terminal => variavel
    novas_variaveis_terminais = {}

    for simbolo, producoes in gramatica.regras.items():
        for prod in producoes:
            simbolos_prod = gramatica.SimbolosProducao(prod)
            if len(simbolos_prod) > 1:
                for idx,c in enumerate(simbolos_prod):
                    if c in gramatica.terminais:
                        if c not in novas_variaveis_terminais:
                            novas_variaveis_terminais[c] = 'G_' + c
                        simbolos_prod[idx] = novas_variaveis_terminais[c]
                        gramatica.regras[simbolo][gramatica.regras[simbolo].index(prod)] = "".join(simbolos_prod)

    # Adiciona as novas variaveis e regras na gramatica
    for terminal,variavel in novas_variaveis_terminais.items():
        add_var = variavel
        gramatica.adicionaVariavel(add_var)
        gramatica.adicionaRegra(add_var, terminal)

    novas_variaveis_producoes = {}
    i=0
    for simbolo, producoes in gramatica.regras.items():
        for idx, prod in enumerate(producoes):
            simbolos_prod = gramatica.SimbolosProducao(prod)
            if(len(simbolos_prod) > 2):
                while (len(simbolos_prod) > 2):
                    reversa = list(reversed(simbolos_prod))
                    ultimo_char = reversa[-1]
                    penultimo_char = reversa[-2]
                    producao_nova = penultimo_char + ultimo_char
                    if producao_nova not in novas_variaveis_producoes:
                        nova_producao = 'D' + str(i)
                        i+=1
                        novas_variaveis_producoes[producao_nova] = nova_producao
                    simbolos_prod.pop()
                    simbolos_prod.pop()
                    simbolos_prod.append(novas_variaveis_producoes[producao_nova])
                producao_substituir = "".join(simbolos_prod)
                gramatica.regras[simbolo][idx] = producao_substituir

    #print(novas_variaveis_producoes)
    # Adiciona as novas variaveis e regras na gramatica
    for producao,variavel in novas_variaveis_producoes.items():
        add_var = variavel
        gramatica.adicionaVariavel(add_var)
        gramatica.adicionaRegra(add_var, producao)

    print(gramatica.regras)
    return gramatica