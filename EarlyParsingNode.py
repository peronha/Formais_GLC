import types
import re

#Um EarlyNode eh um objeto tal que:
#nivel: representa o /numero do algoritmo de Earley
#producao:  producao de uma variavel, ex: S -> aBC, producao: [a, B, C]
#pos_ponteiro: posicao do ponteiro no algoritmo de Earley
class EarlyNode:

    def __init__(self, nivel, pos_ponteiro, producao):
        self.nivel = nivel
        self.pos_ponteiro = pos_ponteiro
        self.producao = producao

    def imprimeNodo(self):
        print("Nivel " + str(self.nivel) + " Posicao: " + str(self.pos_ponteiro) + " Producao " + self.producao)