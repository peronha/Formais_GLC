from FuncoesGramatica import *
from FuncoesEarley import *
# Classe main que determina o fluxo principal do programa.
def main():
    # Carrega a gramática do arquivo de texto.
    gramatica = carregaGramatica('teste1.txt')

    # Remoção de produções vazias.
    #gramatica = RemoveProducoesVazias(gramatica)

    # Remoção de produções unitárias.
    #gramatica = RemoveProducoesUnitarias(gramatica)

    # Remoção de símbolos inúteis.
    #gramatica = RemoveSimbolosInuteis(gramatica)

    # Transformação para a Forma Normal de Chomsky.
    gramatica = FormaNormalChomsky(gramatica)

    print(gramatica.regras)

    EarleyInTheMorning(gramatica, 'aab')
    #EarleyParse(gramatica, 'aab')
    return

main()