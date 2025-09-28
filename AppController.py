import tkinter as tk
from Workspace import Workspace
from Toolbox import Toolbox
from PropertiesPanel import PropertiesPanel
from WidgetTreePanel import WidgetTreePanel  # ← nowy import

class AppController:
    '''Klasa kontrolera, zarządza i komunikuje się z pozostałymi klasami'''
    def __init__(self):
        '''Tworzymy główne okno aplikacji oraz instancje pozostałych klas'''
        self.root = tk.Tk()
        self.root.title("Edytor GUI")
        self.root.geometry("1200x600")

        # Konfiguracja siatki głównego okna
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)  # Workspace rozciąga się

        # Inicjalizacja komponentów z referencją do kontrolera
        self.toolbox = Toolbox(self.root, self)
        self.toolbox.grid(row=0, column=0, sticky="ns")

        self.workspace = Workspace(self.root, self)
        self.workspace.grid(row=0, column=1, sticky="nsew")

        self.properties = PropertiesPanel(self.root, self)
        self.properties.withdraw()  # Ukryj na start

        self.tree_panel = WidgetTreePanel(self.root, self)
        self.tree_panel.grid(row=0, column=2, sticky="ns")

        self.root.mainloop()
