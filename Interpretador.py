from FuncoesGramatica import *

# Classe main que determina o fluxo principal do programa.
def main():

    #nomeArq = input("Entre com o nome do arquivo: ")

    # Carrega a gramática do arquivo de texto.
    #gramatica = carregaGramatica(nomeArq)
    gramatica = carregaGramatica('teste4.txt')

    # Mostra os dados da gramática na tela.
    #print("\nGramática inicial:")
    #gramatica.mostraGramatica()
    #print("\n\nRegras iniciais: " + str(gramatica.regras))

    # Remoção de produções vazias.
    #gramatica = RemoveProducoesVazias(gramatica)

    # Remoção de produções unitárias.
    #gramatica = RemoveProducoesUnitarias(gramatica)

    # Remoção de símbolos inúteis.
    #gramatica = RemoveSimbolosInuteis(gramatica)

    # Transformação para a Forma Normal de Chomsky.
    gramatica = FormaNormalChomsky(gramatica)

    #gramatica.mostraGramatica()

    # Mostra os dados da gramática na tela.
    #print("\n\nRegras após alterações: " + str(gramatica.regras))
    EarleyInTheMorning(gramatica, 'aab')
    return

main()