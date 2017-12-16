from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import font

class Gui:

    def AbrirGramatica(self):
        name = askopenfilename()
        print( name )


    def Sobre(self):
        print("Olá a todos!")

    def  __init__(self):

        self.gui = Tk()
        self.gui.winfo_toplevel().title("Parser de Gramaticas")
        self.gui.minsize(width=650, height=550)
        self.gui.configure(background="white")

        self.criaMenu()
        self.criaForm()
        self.criaCanvas()

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
        w = Canvas(self.gui)
        w.pack(fill='x')

        w.create_line(0, 0, 200, 100)
        w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

        w.create_rectangle(50, 25, 150, 75, fill="blue")


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

    def desenhaArovre(self,arv):
        return
    def imprimeResultado(self,resultado):
        return

If = Gui()


