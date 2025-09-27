import tkinter as tk
from contextlib import nullcontext
from enum import nonmember


class Workspace(tk.Frame):
    '''klasa definiująca główną przestrzeń roboczą
    Tu będą umieszczane komponenty z klasy ToolBox'''
    def __init__(self, master, controller):
        '''do master przekazujemy okno aplikacji (root)
        do controller przekazywany jest AppController'''
        super().__init__(master, bg="white")
        self.controller = controller
        self.pack(side="right", fill="both", expand=True)

        self.widgets = []  # Lista dodanych widgetów
        self.selected_widget = None  # Aktualnie zaznaczony widget
        self._group_vars = {}  # słownik nazw grup → StringVar
        self.containers = [self]  # Workspace jest domyślnym kontenerem
        self.next_column = 0

    def widget_initial_set(self, widget, column, row):
        widget.controller = self.controller
        widget.row = row
        widget.column = column
        widget.rowspan = 1
        widget.columnspan = 1
        widget.sticky = ""
        widget._parent_name = "Workspace"

    def add_widget(self, widget_type):
        '''metoda dodająca widget do przestrzeni roboczej
        :param self klasa okienka (przestrzeń robocza)
        :param widget_type typ komponentu, który jest umieszczany wprzestrzeni roboczej'''
        #w zależności od typu komponentu tworzymy odpowiednie widgety z domyślnymi parametrmi
        if widget_type == "Label":
            widget = tk.Label(self, text="Nowy Label", bg="lightyellow")
            # self.widget_initial_set(widget, self.next_column, 0)
            # widget.grid(column=self.next_column, row=0)
            # Dodanie nowego widgetu do interfejsu
            self.widget_initial_set(widget, self.next_column, 0)
            widget.grid(column=self.next_column, row=0)
            

            # Obsługa kliknięcia — zaznaczenie widgetu
            widget.bind("<Button-1>", lambda e, w=widget: self.select_widget(w))
            # Dodanie do listy
            self.widgets.append(widget)

        elif widget_type == "Button":
            widget = tk.Button(self, text="Nowy Button")
            #self.widget_initial_set(widget)

            # Dodanie nowego widgetu do interfejsu
            self.widget_initial_set(widget, self.next_column, 0)
            widget.grid(column=self.next_column, row=0)

            # Obsługa kliknięcia — zaznaczenie widgetu
            widget.bind("<Button-1>", lambda e, w=widget: self.select_widget(w))
            # Dodanie do listy
            self.widgets.append(widget)

        elif widget_type == "Entry":
            widget = tk.Entry(self)
            #self.widget_initial_set(widget)

            # Dodanie nowego widgetu do interfejsu
            self.widget_initial_set(widget, self.next_column, 0)
            widget.grid(column=self.next_column, row=0)

            # Obsługa kliknięcia — zaznaczenie widgetu
            widget.bind("<Button-1>", lambda e, w=widget: self.select_widget(w))
            # Dodanie do listy
            self.widgets.append(widget)

        elif widget_type == "Checkbutton":
            var = tk.BooleanVar(value=False)
            widget = tk.Checkbutton(self, text="Opcja", variable=var)
            #self.widget_initial_set(widget)

            # zapisz zmienną przechowującą stan (on/off) w obiekcie widgetu
            widget._linked_var = var
            # Dodanie nowego widgetu do interfejsu
            self.widget_initial_set(widget, self.next_column, 0)
            widget.grid(column=self.next_column, row=0)

            # Obsługa kliknięcia — zaznaczenie widgetu
            widget.bind("<Button-1>", lambda e, w=widget: self.select_widget(w))
            # Dodanie do listy
            self.widgets.append(widget)

        elif widget_type == "Radiobutton":
            widget = tk.Radiobutton(self, text="Opcja", value="Opcja")
            #self.widget_initial_set(widget)

            widget._linked_var = tk.StringVar()
            widget.config(variable=widget._linked_var)
            widget.controller = self.controller  # ← dodaj to!
            self.widget_initial_set(widget, self.next_column, 0)
            widget.grid(column=self.next_column, row=0)
            widget.bind("<Button-1>", lambda e, w=widget: self.select_widget(w))
            self.widgets.append(widget)

        elif widget_type == "Frame":
            widget = tk.Frame(self, bg="lightgray", bd=2, relief="groove", width=200, height=100)
            #self.widget_initial_set(widget)

            widget.pack_propagate(False)  # ← zapobiega automatycznemu dopasowaniu do zawartości

            # Każdy kontener powinien mieć atrybut _name, żeby było wiadomo na czym osadzamy widget
            widget._name = f"Frame_{len(self.containers)}"
            # dodaję do listy kontenerów czyli komponentów, na których można osadzać inne widgety
            self.containers.append(widget)
            print(widget.winfo_name())
            self.widget_initial_set(widget, self.next_column, 0)
            widget.grid(column=self.next_column, row=0)
            widget.bind("<Button-1>", lambda e, w=widget: self.select_widget(w))
            self.widgets.append(widget)

        elif widget_type == "LabelFrame":
            widget = tk.LabelFrame(self, text="Grupa", bg="lightgray", bd=2, relief="ridge", width=200, height=100)
            #self.widget_initial_set(widget)

            widget.pack_propagate(False)

            # Każdy kontener powinien mieć atrybut _name, żeby było wiadomo na czym osadzamy widget
            widget._name = f"Frame_{len(self.containers)}"
            # dodaję do listy kontenerów czyli komponentów, na których można osadzać inne widgety
            self.containers.append(widget)
            self.widget_initial_set(widget, self.next_column, 0)
            widget.grid(column=self.next_column, row=0)
            widget.bind("<Button-1>", lambda e, w=widget: self.select_widget(w))
            self.widgets.append(widget)

        else:
            return  # nieobsługiwany typ
        self.next_column +=1

    def select_widget(self, widget):
        '''Obsługa zdarzenia kliknięcia na widget
        do atrybutu selected_widget jest przypisywany kliknięty widget
        a następnie pokazywane jest okienko z własciwościami widgetu'''
        self.selected_widget = widget
        self.controller.properties.display_properties(widget)

    def update_widget_property(self, key, value):
        '''metoda aktualizująca właściwości widgetu
        przypisuje do atrybutu config wybranego widgetu par klucz, wartość
        wygląda nie wykorzystywaną'''
        if self.selected_widget:
            try:
                self.selected_widget.config({key: value})
            except Exception as e:
                print(f"Błąd przy aktualizacji właściwości: {e}")

    def assign_group_variable(self, widget, group_name):
        if group_name not in self._group_vars:
            var = tk.StringVar()
            var.name = group_name
            self._group_vars[group_name] = var
        widget._linked_var = self._group_vars[group_name]
        widget.config(variable=widget._linked_var)

    def get_parent_container(self, parent_name):
        for container in self.containers:
            # current_name = container.winfo_name()
            widget_name = container._name
            if widget_name==parent_name:
                return container
        return

    def reparent_widget(self, widget, parent_name):
        #widget.reparent(parent_name)
        #widget.grid_forget()
        parent_widget = self.get_parent_container(parent_name)
        #parent_name = parent_widget.winfo_name()
        widget.grid(column=0, row=0, in_=parent_widget)
        widget._parent_name = parent_name


    # def reparent_widget(self, widget, parent_name):
    #     for container in self.containers:
    #         if getattr(container, "_name", "Workspace") == parent_name:
    #             widget.grid_forget()
    #             widget.pack_forget()
    #             widget.master = container
    #             widget._parent_name = parent_name
    #
    #             # 🔒 Jeśli kontener to Workspace → użyj pack()
    #             if container == self:
    #                 self.widget_initial_set(widget, self.next_column, 0)
    #                 widget.grid(column=self.next_column, row=0)
    #             else:
    #                 # 🧠 Użyj grid() tylko w kontenerach innych niż Workspace
    #                 widget.grid(
    #                     row=widget.row,
    #                     column=widget.column,
    #                     rowspan=widget.rowspan,
    #                     columnspan=widget.columnspan,
    #                     sticky=widget.sticky
    #                 )
    #             returned







