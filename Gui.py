from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import font
import math

class Gui:

    def AbrirGramatica(self):
        name = askopenfilename()
        print( name )


    def Sobre(self):
        print("Olá a todos!")

    def  __init__(self, tam_x, tam_y):
        self.tamx = tam_x
        self.tamy = tam_y
        self.gui = Tk()
        self.gui.winfo_toplevel().title("Parser de Gramaticas")
        self.gui.minsize(width=tam_x, height=tam_y)
        self.gui.configure(background="white")

        self.criaMenu()
        self.criaForm()
        self.canvas = self.criaCanvas()
        self.desenhaArvore(0)
        mainloop()

    def criaForm(self):

        box1 = Frame(self.gui, bg='#a1dbcd', borderwidth=4, relief=GROOVE)
        box1.pack(fill='x')

        fonte = font.Font(family='Playbill', size=22)
        fonte2 = font.Font(family='Playbill', size=16)
        l1 = Label(box1,bg='#a1dbcd', font=fonte,  text="Palavra a ser reconhecida: ", fg="#383a39")
        l1.pack(padx=20, pady=10, side=LEFT,anchor='nw')

        e1 = Entry(box1,cursor="heart",   width=40)
        e1.pack(padx=30, pady=18, side=LEFT, anchor='nw')

        box2  = Frame(self.gui, bg='#a1dbcd',borderwidth=4, relief=GROOVE)
        box2.pack(fill='x')

        b1 = Button(box2, text="Reconhecer", command=self.reconhecePalavra, fg="#a1dbcd", bg="#383a39", font = fonte2)
        b1.pack(padx=20, pady=10, side=LEFT, anchor='nw')

        b2 = Button(box2, text="Imprimir Gramatica", command=self.reconhecePalavra,  fg="#a1dbcd", bg="#383a39", font = fonte2)
        b2.pack(padx=10, pady=10, side=LEFT, anchor='nw')

        b3 = Button(box2, text="Imprimir Arvores", command=self.reconhecePalavra,  fg="#a1dbcd", bg="#383a39", font = fonte2)
        b3.pack(padx=10, pady=10, side=LEFT, anchor='nw')


    def reconhecePalavra(self):
        print("click click")

    def criaCanvas(self):
        c = Canvas(self.gui,  height='500')
        c.pack(fill='x')

        return c

    def criaMenu(self):

        menu = Menu(self.gui)
        self.gui.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="Gramatica", menu=filemenu)
        filemenu.add_command(label="Carregar Gramatica", command=self.AbrirGramatica)
        filemenu.add_separator()
        filemenu.add_command(label="Sair", command=self.gui.quit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Ajuda", menu=helpmenu)
        helpmenu.add_command(label="Sobre...", command=self.Sobre)


    def desenhaGalhoDir(self, x, y, tam):
        angulo = math.pi/3

        x1 = x + int(math.cos(angulo) * tam)
        y1 = y + int(math.sin(angulo) * tam) + 15
        #print(x1)
        #print(y1)
        # Draw the line
        self.canvas.create_line(x-2, y , x1, y1, tags="line")


    def desenhaGalhoEsq(self, x, y, tam):
        angulo = math.pi/3

        x1 = x - int(math.sin(angulo) * tam)
        y1 = y + int(math.cos(angulo) * tam) + 19
        self.canvas.create_line(x, y  , x1  , y1, tags="line")


    def desenhaNodoDir(self, simbolo,x ,y, prof):
        x = x +  20 * prof
        y = y + 50 * prof
        #Verificar se é terminal
        if simbolo == 'a':
            self.canvas.create_oval(x,y,x-20, y-20, fill='red')
            self.canvas.create_text(x-11, y-10, fill="white", font="Playbill 12 italic bold",
                                    text="a")
        else:
            self.canvas.create_oval(x,y,x-20, y-20, fill='green')
            self.canvas.create_text(x-11, y-10, fill="white", font="Playbill 12 italic bold",
                                    text="B")


    def desenhaNodoEsq(self, simbolo, x, y, prof):

        x = x - 24 * prof
        y = y + 50 * prof
        if simbolo == 'a':
            self.canvas.create_oval(x,y,x-20, y-20, fill='red')
            self.canvas.create_text(x-11, y-10, fill="white", font="Playbill 12 italic bold",
                                    text="a")
        else:
            self.canvas.create_oval(x,y,x-20, y-20, fill='green')
            self.canvas.create_text(x-11, y-10, fill="white", font="Playbill 12 italic bold",
                                    text="B")

    def desenhaArvore(self,arv):
        meio = self.tamx/2
        altura = 40
        #Desenha Simbolo Inicial
        self.canvas.create_oval(meio,altura,meio-20, altura-20, fill='green')
        self.canvas.create_text(meio-11, altura-10, fill="white", font="Playbill 12 italic bold",
                                text="S")

        self.desenhaGalhoEsq(meio-20, altura , 15)
        self.desenhaGalhoDir(meio, altura, 15)

        self.desenhaNodoEsq('a', meio, altura, 1)
        self.desenhaNodoDir('B', meio, altura, 1)

        #profundidade = 2
        self.desenhaNodoEsq('a', meio, altura + 20, 2)
        self.desenhaNodoDir('B', meio , altura + 20, 2)

        self.desenhaNodoEsq('a', meio + ( 20 *2) , altura + 20, 2)
        self.desenhaNodoDir('B', meio - (14 * 2), altura + 20, 2)

        self.desenhaNodoEsq('a', meio, altura + 20, 2)
        self.desenhaNodoDir('B', meio , altura + 20, 2)

        self.desenhaNodoEsq('a', meio + ( 20 *2) , altura + 20, 2)
        self.desenhaNodoDir('B', meio - (14 * 2), altura + 20, 2)



        return
    def imprimeResultado(self,resultado):
        return

If = Gui(650, 500)


