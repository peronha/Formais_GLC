from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import font
from Gramatica import *
from BinarySearchTree import *
from FuncoesGramatica import *
import math

class Gui:
    def  __init__(self, tam_x, tam_y):
        self.tamx = tam_x
        self.tamy = tam_y
        self.gui = Tk()
        self.gui.winfo_toplevel().title("Parser de Gramaticas")
        self.gui.minsize(width = tam_x, height = tam_y)
        self.gui.configure(background = "white")

        self.janelaLargura = 1200 #self.gui.winfo_screenwidth() # Deixa a janela com a largura da tela.
        self.janelaAltura = 800 #self.gui.winfo_screenheight() # Deixa a janela com a altura da tela.
        self.gui.geometry("%dx%d+0+0" % (self.janelaLargura, self.janelaAltura))

        self.gramatica = Gramatica()

        # Para teste:
        self.gramatica.terminais = ['a', 'b']
        self.gramatica.variaveis = ['S', 'A', 'B']

        self.CriaMenu()
        self.CriaForm()
        self.canvas = self.CriaCanvas()
        mainloop()

    # Cria os elementos da janela.
    def CriaForm(self):

        # Definição das fontes.
        fonteDestaque = font.Font(family = 'Helvetica', size = 18)

        # Cria o frame com a entrada da palavra a ser reconhecida.
        frameEntrada = Frame(self.gui, background = '#2F5866', padx = 60, pady = 20)
        frameEntrada.pack(fill = 'x')

        # Label para entrada de texto.
        labelEntradaPalavra = Label(frameEntrada, background = '#2F5866', font = fonteDestaque, text = "Palavra a ser reconhecida:", fg = "#FFFFFF")
        labelEntradaPalavra.pack(side = LEFT, anchor = 'nw')

        # Cria a entrada de texto para palavra a ser reconhecida.
        entradaPalavra = Entry(frameEntrada, cursor = "heart", width = 40)
        entradaPalavra.pack(side = LEFT, anchor = 'nw', padx = 10, pady = 7)

        # Cria o frame com os botões.
        frameBotoes = Frame(self.gui, bg = '#2F5866')
        frameBotoes.pack(fill = 'x')

        # Botão Reconhecer.
        botao1 = self.BotaoPadrao(frameBotoes, "Reconhecer palavra", self.ReconhecerPalavra)
        botao1.pack(side = LEFT)

        # Botão Imprimir Gramática.
        botao2 = self.BotaoPadrao(frameBotoes, "Imprimir gramática", self.ImprimeGramatica)
        botao2.pack(side = LEFT)

        # Botão Imprimir Árvores.
        botao3 = self.BotaoPadrao(frameBotoes, "Imprimir árvores", self.ImprimeArvore)
        botao3.pack(side = LEFT)

    # Retorna um botão com as configurações padrão.
    def BotaoPadrao(self, elementoPai, textoBotao, comando):
        fundoCor = "#444444"
        fundoCorAtivo = "#222222"
        letraCor = "#FFFFFF"
        letraCorAtivo = "#FFFFFF"
        bordaLargura = 1
        fonteTamanho = 12
        fonteFamilia = "Helvetica"
        largura = math.ceil(30/278 * (self.janelaLargura / 3))
        altura = 1

        fonte = font.Font(family=fonteFamilia, size=fonteTamanho)
        novoBotao = Button(elementoPai,
                           text=textoBotao,
                           command=comando,
                           font=fonte,
                           background=fundoCor,
                           activebackground=fundoCorAtivo,
                           foreground=letraCor,
                           activeforeground=letraCorAtivo,
                           borderwidth=bordaLargura,
                           width=largura,
                           height=altura)

        return novoBotao

    # Lê arquivo com gramática.
    def AbrirGramatica(self):
        name = askopenfilename()
        self.gramatica = carregaGramatica(name)

    # Executa o reconhecimento da palavra inserida.
    def ReconhecerPalavra(self):
        self.canvas.delete("all")
        print("Você clicou em \"Reconhecer palavra\".")

    # Executa o reconhecimento da palavra inserida.
    def ImprimeGramatica(self):
        self.canvas.delete("all")

        self.gramatica = FormaNormalChomsky(self.gramatica)

        self.DesenhaGramatica()

    # Executa o reconhecimento da palavra inserida.
    def ImprimeArvore(self):
        self.canvas.delete("all")
        self.DesenhaArvore(0)

    # Crie o canvas para exibição dos resultados.
    def CriaCanvas(self):
        c = Canvas(self.gui, width = self.janelaLargura, height = self.janelaAltura)
        c.pack()

        return c

    def CriaMenu(self):
        menu = Menu(self.gui)
        self.gui.config(menu = menu)
        filemenu = Menu(menu, tearoff = 0)
        menu.add_cascade(label = "Gramatica", menu = filemenu)
        filemenu.add_command(label = "Carregar gramática", command = self.AbrirGramatica)
        filemenu.add_separator()
        filemenu.add_command(label = "Sair", command = self.gui.quit)

        helpmenu = Menu(menu, tearoff = 0)
        menu.add_cascade(label = "Ajuda", menu = helpmenu)
        helpmenu.add_command(label = "Sobre...", command = self.Sobre)

    def Sobre(self):
        print("Olá a todos!")

    # Desenha um nodo.
    def DesenhaNodo(self, xCentro, yCentro, raio, simbolo):
        cor = "#FFFFFF"

        if simbolo in self.gramatica.variaveis:
            cor = "#B20000"
        elif simbolo in self.gramatica.terminais:
            cor = "#005900"

        tamanhoFonte = int((7 * raio - 4) / 8)

        self.canvas.create_oval(xCentro - raio, yCentro - raio, xCentro + raio, yCentro + raio, fill = cor)
        self.canvas.create_text(xCentro, yCentro, fill = "white", font = "Helvetica " + str(tamanhoFonte) + " bold", text = simbolo)

    # Desenha todos os nodos da árvore binária.
    def DesenhaNodos(self, raiz, xCentro, yCentro, raioNodo, espacamentoX, espacamentoY):
        if raiz.leftChild is not None:
            self.DesenhaNodos(raiz.leftChild, xCentro - espacamentoX * raioNodo, yCentro + espacamentoY * raioNodo, raioNodo, espacamentoX * 0.5, espacamentoY)
        self.DesenhaNodo(xCentro, yCentro, raioNodo, raiz.val)
        if raiz.rightChild is not None:
            self.DesenhaNodos(raiz.rightChild, xCentro + espacamentoX * raioNodo, yCentro + espacamentoY * raioNodo, raioNodo, espacamentoX * 0.5, espacamentoY)

    # Desenha todos os galhos da árvore binária.
    def DesenhaGalhos(self, raiz, xCentro, yCentro, raioNodo, espacamentoX, espacamentoY, direcao):
        if raiz.leftChild is not None:
            self.DesenhaGalhos(raiz.leftChild, xCentro - espacamentoX * raioNodo, yCentro + espacamentoY * raioNodo, raioNodo, espacamentoX * 0.5, espacamentoY, "L")
        deslocamentoGalho = raioNodo / 1.41
        if direcao == "L":
            xFinal = (xCentro + espacamentoX * 2 * raioNodo) - deslocamentoGalho
            yFinal = (yCentro - espacamentoY * raioNodo) + deslocamentoGalho
            self.canvas.create_line(xCentro + deslocamentoGalho, yCentro - deslocamentoGalho, xFinal, yFinal, tags = "line")
        if raiz.rightChild is not None:
            self.DesenhaGalhos(raiz.rightChild, xCentro + espacamentoX * raioNodo, yCentro + espacamentoY * raioNodo, raioNodo, espacamentoX * 0.5, espacamentoY, "R")
        if direcao == "R":
            xFinal = (xCentro - espacamentoX * 2 * raioNodo) + deslocamentoGalho
            yFinal = (yCentro - espacamentoY * raioNodo) + deslocamentoGalho
            self.canvas.create_line(xCentro - deslocamentoGalho, yCentro - deslocamentoGalho, xFinal, yFinal, tags = "line")

    # Desenha a árvore binária de derivação.
    def DesenhaArvore(self, arvore):
        # Para testes:
        self.canvas.create_text(self.canvas.winfo_width() / 2, 30, fill="black", font="Helvetica 12 bold",
                                text="Árvore para testes:")
        arvore = self.CriaArvoreTeste()
        # Fim testes.

        alturaArvore = arvore.GetHeight() + 1

        # Define o tamanho de cada nodo.
        raioNodo = (-2) * alturaArvore + 22
        if raioNodo < 8:
            raioNodo = 8

        espacamentoX = 4 * alturaArvore
        espacamentoY = 4

        # Define qual é o meio da tela.
        meio = self.canvas.winfo_width() / 2
        inicioY = 60

        self.DesenhaNodos(arvore.root, meio, inicioY, raioNodo, espacamentoX, espacamentoY)
        self.DesenhaGalhos(arvore.root, meio, inicioY, raioNodo, espacamentoX, espacamentoY, None)

        return

    # Apresenta a gramática lida no canvas.
    def DesenhaGramatica(self):
        xCentro = self.canvas.winfo_width() / 2
        yInicial = 30

        contadorLinha = 0

        if self.gramatica.inicial is None:
            self.canvas.create_text(xCentro, yInicial, fill = "black", font = "Helvetica 12 bold", text = "A gramática lida não é válida.")
        else:
            linha = "G = ({"
            for contador in range (0, len(self.gramatica.variaveis)):
                linha += self.gramatica.variaveis[contador]
                if contador != len(self.gramatica.variaveis) - 1:
                    linha += ", "
            linha += "}, {"
            for contador in range (0, len(self.gramatica.terminais)):
                linha += self.gramatica.terminais[contador]
                if contador != len(self.gramatica.terminais) - 1:
                    linha += ", "
            linha += "}, P, " + self.gramatica.inicial + ") onde "
            self.canvas.create_text(xCentro, yInicial, fill = "black", font = "Helvetica 12 bold", text = linha)
            contadorLinha += 2
            linha = "P = {"
            contadorSimbolo = 0
            for simbolo in self.gramatica.regras:
                contadorProducao = 0
                for producao in self.gramatica.regras[simbolo]:
                    linha += simbolo + " => " + producao
                    if (contadorSimbolo != len(self.gramatica.regras) - 1) or (contadorProducao != len(self.gramatica.regras[simbolo]) - 1):
                        linha += ",\n"
                    else:
                        linha += "}"
                    self.canvas.create_text(xCentro, yInicial + 30 * contadorLinha, fill = "black", font = "Helvetica 12 bold", text = linha)
                    contadorLinha += 1
                    linha = ""
                    contadorProducao += 1
                contadorSimbolo += 1

    # Cria uma árvore binária de derivação para testes.
    def CriaArvoreTeste(self):
        arvore = BinaryTree()
        arvore.setRoot("S")

        nodoA = arvore.InsertLeftNode(arvore.root, "A")
        nodoB = arvore.InsertRightNode(arvore.root, "B")

        arvore.InsertLeftNode(nodoA, "a")

        nodoA = arvore.InsertLeftNode(nodoB, "B")
        nodoB = arvore.InsertRightNode(nodoB, "A")

        arvore.InsertLeftNode(nodoA, "b")

        nodoA = arvore.InsertLeftNode(nodoB, "B")
        nodoB = arvore.InsertRightNode(nodoB, "A")

        arvore.InsertLeftNode(nodoA, "b")
        arvore.InsertLeftNode(nodoB, "a")

        return arvore

If = Gui(650, 500)