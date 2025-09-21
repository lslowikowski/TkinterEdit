import tkinter as tk
from Workspace import Workspace
from Toolbox import Toolbox
from PropertiesPanel import PropertiesPanel

class AppController:
    '''Klasa kontrolera, zarządza
    i komunikuje się z pozostałymi klasami'''
    def __init__(self):
        '''Tworzymy główne okno aplikacji
        oraz tworzymy instancje pozostałych klas
        przekazując im referencję do kontrolera'''
        self.root = tk.Tk()
        self.root.title("Edytor GUI")
        self.root.geometry("1000x600")

        # Inicjalizacja komponentów z referencją do kontrolera
        self.workspace = Workspace(self.root, self)
        self.toolbox = Toolbox(self.root, self)
        self.properties = PropertiesPanel(self.root, self)
        self.properties.withdraw()

        self.root.mainloop()
