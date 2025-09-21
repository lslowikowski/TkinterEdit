import tkinter as tk
from widget_config import WIDGET_PROPERTIES

class PropertiesPanel(tk.Toplevel):
    ''' Klasa obsługująca panel (a właściwie okienko) z właściwościami widgetu'''
    def __init__(self, master, controller):
        # do master przekazujemy okno aplikacji (root)
        # do controller przekazywany jest AppController
        super().__init__(master)
        self.controller = controller
        self.title("Właściwości")
        self.geometry("300x200")
        #self.protocol("WM_DELETE_WINDOW", self.__callback) #wskazanie metody zamykającej okno - nie pozwala
        # wskazanie metody zamykającej okno - zamiast zamknięcia ukrywa okno właściwości
        self.protocol("WM_DELETE_WINDOW", lambda: self.__callback(self))
        #przy inicjalizacji nie mamy wybranego widgetu stąd none
        self.selected_widget = None
        self.fields = {}  # słownik pól właściwości, przy inicjalizacji pusty

    @staticmethod
    def __callback(self):
        #zamiast zamykać okno, ukrywamy je
        self.withdraw()
        return

    def display_properties(self, widget):
        #metoda pokazująca właściwości wybranego widgetu
        # 🧭 Ustawienie pozycji okna względem klikniętego widgetu
        x = widget.winfo_rootx()
        y = widget.winfo_rooty()
        self.geometry(f"+{x + 20}+{y + 20}")  # lekki offset, żeby nie zasłaniać widgetu
        self.deiconify() #visible=true - okienko własciwości się pokazuje
        self.wm_attributes("-topmost", 1) #okienko z właściwościami na wierzch
        self.selected_widget = widget #wskazujemy wybrany widget

        # Wyczyść pokazywane atrybuty poprzedniego widgetu
        for child in self.winfo_children():
            child.destroy()

        tk.Label(self, text=f"Właściwości: {type(widget).__name__}").pack() #pokazanie nazwy widgetu
        self.fields = {} #inicjalizacja listy atrybutów

        widget_type = type(widget).__name__  #ustawienie typu widgetu
        # pobranie do zmiennej props jsona z listą właściwości konkretnego typu widgetu
        props = WIDGET_PROPERTIES.get(widget_type, {})

        #wyświetlamy właściwość po właściwości w okienku
        for prop_name, config in props.items():
            tk.Label(self, text=prop_name).pack() #nazwa właściwości
            #jeżeli jet to właściwość, którą można wprowadzić w polu edycyjnym
            if config["type"] == "entry":
                entry = tk.Entry(self) #dodjemy pole typu entry
                entry.pack()

                #Tworzy pole tekstowe (entry) i wstawia do niego aktualną wartość właściwości danego widgetu.
                #config["getter"] to funkcja, która wie, jak pobrać daną właściwość z widgetu.
                entry.insert(0, config["getter"](widget))

                #Zapisuje pole edycji (entry) oraz funkcję setter do słownika self.fields.
                #Dzięki temu później, w apply_changes(), można:
                 #- pobrać wartość z pola (entry.get())
                 #- użyć setter(widget, value) do aktualizacji właściwości
                self.fields[prop_name] = (entry, config["setter"])

            #jeżeli jet to właściwość, typu checkbox
            elif config["type"] == "checkbox":
                #zmienna przechowująca wartość checkboxa
                var = tk.BooleanVar(value=config["getter"](widget))
                checkbox = tk.Checkbutton(self, variable=var) #dodajemy pole typu checkbox
                checkbox.pack()
                #wskazujemy setter do ustawiania właściwości - patrz wyżej
                self.fields[prop_name] = (var, config["setter"])
            # jeżeli jet to właściwość, typu dropdown - rozwijana lista opcji
            elif config["type"] == "dropdown":
                options = config["options"](widget)
                # zmienna przechowująca wartość radiobuttonów ustawiana na wartość początkową
                # na podstawie funkcji getter, czyli aktualnej wartości właściwości w edytowanym widgetcie
                var = tk.StringVar(value=config["getter"](widget))
                #Tworzy rozwijane menu (OptionMenu) z listą opcji.
                dropdown = tk.OptionMenu(self, var, *options)
                dropdown.pack()
                self.fields[prop_name] = (var, config["setter"])

        tk.Button(self, text="Zastosuj", command=self.apply_changes).pack(pady=10)

    def apply_changes(self):
        for prop_name, (field, setter) in self.fields.items():
            try:
                # Pobierz wartość z pola (Entry lub Variable)
                value = field.get() if hasattr(field, "get") else None

                # Zastosuj setter
                setter(self.selected_widget, value)
            except Exception as e:
                print(f"Błąd przy ustawianiu {prop_name}: {e}")
        self.withdraw()
