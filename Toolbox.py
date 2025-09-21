import tkinter as tk

class Toolbox(tk.Frame):
    ''' Klasa zawierająca przyciski, które pozwalają na dodanie widgetów do Workspace'''
    def __init__(self, master, controller):
        #do master przekazujemy okno aplikacji (root)
        #do controller przekazywany jest AppController
        super().__init__(master, bg="lightgray", width=200)
        self.controller = controller
        self.pack(side="left", fill="y")
        '''Definicja przycisków dodających poszczególne widgety do Workspace
        w wyniku wybrania przycisku z toolboox wywoływana jest metoda workspace.add_widget(typ_widgetu)'''
        tk.Button(self, text="Dodaj Label", command=lambda: self.controller.workspace.add_widget("Label")).pack(pady=5)
        tk.Button(self, text="Dodaj Button", command=lambda: self.controller.workspace.add_widget("Button")).pack(pady=5)
        tk.Button(self, text="Dodaj Entry", command=lambda: self.controller.workspace.add_widget("Entry")).pack(pady=5)
        tk.Button(self, text="Dodaj Checkbutton", command=lambda: self.controller.workspace.add_widget("Checkbutton")).pack(pady=5)
        tk.Button(self, text="Dodaj Radiobutton", command=lambda: self.controller.workspace.add_widget("Radiobutton")).pack(pady=5)
        tk.Button(self, text="Dodaj Frame", command=lambda: self.controller.workspace.add_widget("Frame")).pack(pady=5)
        tk.Button(self, text="Dodaj LabelFrame", command=lambda: self.controller.workspace.add_widget("LabelFrame")).pack(pady=5)

