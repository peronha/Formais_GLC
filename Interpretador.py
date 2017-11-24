from FuncoesGramatica import *


def main():

    nomeArq = input("Entre com o nome do arquivinho: ")

    gr = carregaGramatica(nomeArq)

    gr.mostraGramatica()

    return


main()