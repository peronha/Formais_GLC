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

# Remove as produções vazias e adiciona produções para compensar.
def RemoveProducoesVazias(gramatica):
    # Gera conjunto das variáveis que produzem direta ou indiretamente a palavra vazia.
    conjuntoProducoesVazias = gramatica.ProducoesVazias('V')

    # Exclui as produções diretamente vazias e adiciona as produções que compensam.
    if len(conjuntoProducoesVazias) > 0:
        novasProducoes = {}
        for cabeca in gramatica.regras:
            novasProducoes[cabeca] = []
            for producao in gramatica.regras[cabeca]:
                for simbolo in conjuntoProducoesVazias:
                    if (len(producao) > 1) and (simbolo in producao):
                        # Identifica quais os índices da string que possuem o símbolo procurado.
                        indicesVazios = [pos for pos, char in enumerate(producao) if char in conjuntoProducoesVazias]
                        # Indica quantas vezes o símbolo aparece dentro da string.
                        numeroSimbolosVazios = len(indicesVazios)
                        for contador in range(0, 2**numeroSimbolosVazios - 1):
                            # Correção da string que representa o número binário.
                            contadorBinario = bin(contador).replace("0b", "")
                            for diferencaTamanho in range(0, numeroSimbolosVazios - len(contadorBinario)):
                                contadorBinario = contadorBinario.replace(contadorBinario, "0" + contadorBinario)
                            # Para cada zero do número binário o símbolo será apagado na nova produção no local indicado.
                            novaProducao = producao
                            for indiceBinario in range(len(contadorBinario) - 1, -1, -1):
                                if contadorBinario[indiceBinario] == "0":
                                    # Apaga o símbolo no local correspondente com a variável indicesVazios.
                                    novaProducao = novaProducao[:indicesVazios[indiceBinario]] + novaProducao[indicesVazios[indiceBinario]+1:]
                            # Só adiciona a produção caso ela ainda não exista.
                            if (novaProducao not in novasProducoes[cabeca]) and (novaProducao != ""):
                                novasProducoes[cabeca].append(novaProducao)
                if 'V' == producao:
                    gramatica.regras[cabeca].remove(producao)

        for cabeca in gramatica.regras:
            if cabeca in novasProducoes and len(novasProducoes[cabeca]) > 0:
                for novaProducao in novasProducoes[cabeca]:
                    gramatica.regras[cabeca].append(novaProducao)

    return gramatica

# Remove todas as produções do Tipo A -> B
def RemoveProducoesUnitarias(gramatica):

    fecho_transitivo = gramatica.FechoTransitivo()

    # exclui as producoes de simbolos
    for simbolo,producoes in gramatica.regras.items():
        for prod in producoes[:]:
            if prod in gramatica.variaveis:
                gramatica.regras[simbolo].remove(prod)

    # Inclui as producoes do Fecho Transitivo nas variaveis da gramatica
    for  simb,prod  in fecho_transitivo.items():
        if len(prod) > 0:
            for v in prod:
                if v in gramatica.regras:
                    for v_prod in gramatica.regras[v]:
                        if v_prod not in gramatica.regras[simb]:
                            gramatica.regras[simb].append(v_prod)

    return gramatica

# Remove os símbolos não atingíveis e símbolos não geradores.
def RemoveSimbolosInuteis(gramatica):

    simbolosGeradores = gramatica.SimbolosGeradores()

    # Remove símbolos não geradores.
    producoesExcluidas = {}
    for simbolo in gramatica.variaveis:
        producoesExcluidas[simbolo] = []
        if simbolo not in simbolosGeradores:
            for cabeca, producoes in gramatica.regras.items():
                for producao in producoes:
                    if simbolo in producao:
                        producoesExcluidas[cabeca].append(producao)
            for cabeca, producoesExcluidas in producoesExcluidas.items():
                for producaoExcluida in producoesExcluidas:
                    gramatica.regras[cabeca].remove(producaoExcluida)

    simbolosAtingiveis = gramatica.SimbolosAtingiveis()

    # Remove símbolos não atingíveis.
    for simbolo in gramatica.variaveis:
        if (simbolo not in simbolosAtingiveis) and (simbolo in gramatica.regras):
            del gramatica.regras[simbolo]

    return gramatica
def substituiSimbolos(simbolos,antigo, novo):

    for idx, c, in enumerate(simbolos):
        if c == antigo:
            simbolos[idx] = novo

    return simbolos
def FormaNormalChomsky(gramatica):
    gramatica = RemoveProducoesVazias(gramatica)
    #print("\nRegras da gramática após remoção de palavras vazias: \n" + str(gramatica.regras))

    gramatica = RemoveProducoesUnitarias(gramatica)
    #print("\nRegras da gramática após remoção de produções unitárias: \n" + str(gramatica.regras))

    gramatica = RemoveSimbolosInuteis(gramatica)
    #print("\nRegras da gramática após remoção de símbolos inúteis: \n" + str(gramatica.regras))

    #print(gramatica.terminais)

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
                        simbolos_prod = substituiSimbolos(simbolos_prod, c, novas_variaveis_terminais[c])
                        gramatica.regras[simbolo][gramatica.regras[simbolo].index(prod)] = "".join(simbolos_prod)
                        prod = "".join(simbolos_prod)

    # Adiciona as novas variaveis e regras na gramatica
    for terminal,variavel in novas_variaveis_terminais.items():
        add_var = variavel
        gramatica.adicionaVariavel(add_var)
        gramatica.adicionaRegra(add_var, terminal)

    novas_variaveis_producoes = {}
    i=0
    #TODO testar mais casos e verificar direito esta porcaria
    for simbolo, producoes in gramatica.regras.items():
        for idx, prod in enumerate(producoes):
            simbolos_prod = gramatica.SimbolosProducao(prod)
            if(len(simbolos_prod) > 2):
                while (len(simbolos_prod) > 2):
                    #reversa = list(reversed(simbolos_prod))
                    #print(reversa)
                    ultimo_char = simbolos_prod[-1]
                    penultimo_char = simbolos_prod[-2]
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

    #print("\nGramática na Forma Normal de Chomsky: \n")
    #gramatica.mostraGramatica()
    return gramatica

#S → NP VP NP → NP PP
#PP → P NP NP → N
#VP → V NP N → astronomers
#VP → VP PP N → ears
#P → with N → stars
#V → saw N → telescopes
#Earley is not picky about what type of grammar it accepts :)
def EarleyInTheMorning(gramatica, palavra):
    produzConjInicial(gramatica)

    return 0

def verificaRegras(var):
    return

def produzConjInicial(gramatica):
    gramatica.regras
    chart = {}
    chart[0] = gramatica.regras['S']
    continua = 1

    print(chart)