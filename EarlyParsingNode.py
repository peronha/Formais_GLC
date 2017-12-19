import types
import re

class ConjuntoProducoes:
    def __init__(self, nivel):
        self.nivel = nivel
        self.producoesCima = []
        self.producoesBaixo = []

    def AdicionaProducaoCima(self, producaoEarley):
        self.producoesCima.append(producaoEarley)

    def AdicionaProducaoBaixo(self, producaoEarley):
        self.producoesBaixo.append(producaoEarley)

class ProducaoEarley:
    def __init__(self, cabeca, producao, indice, posicaoMarcador, gramatica):
        self.indice = indice
        if posicaoMarcador >= len(producao):
            self.posicaoMarcador = len(producao) - 1
        elif posicaoMarcador <= 0:
            self.posicaoMarcador = 0
        else:
            self.posicaoMarcador = posicaoMarcador
        self.cabeca = cabeca

        self.producao = producao

        self.posicoesMarcador = []
        self.ConfiguraMarcador(gramatica)

        self.producao = producao[:posicaoMarcador] + "." + producao[posicaoMarcador:]

    # Configura possíveis posições para o marcador.
    def ConfiguraMarcador(self, gramatica):
        # Seleciona as posições na string de acordo com as variáveis.
        for variavel in gramatica.variaveis:
            try:
                self.posicoesMarcador.append(self.producao.index(variavel))
            except ValueError:
                pass

        # Seleciona as posições na string de acordo com os terminais.
        if len(self.posicoesMarcador) < 2:
            for terminal in gramatica.terminais:
                try:
                    self.posicoesMarcador.append(self.producao.index(terminal))
                    break
                except ValueError:
                    pass

        # Adiciona a última posição da string como sendo uma possível posição para o marcador.
        self.posicoesMarcador.append(len(self.producao))

    # Move o marcador para a próxima posição.
    def AvancaMarcador(self):
        self.producao.replace(".", "")
        self.posicaoMarcador += 1
        if self.posicaoMarcador < len(self.posicoesMarcador):
            self.producao = self.producao[:self.posicaoMarcador] + "." + self.producao[self.posicaoMarcador:]


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