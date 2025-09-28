import tkinter as tk
from WidgetNode import WidgetNode


class Workspace(tk.Frame):
    '''klasa definiująca główną przestrzeń roboczą
    Tu będą umieszczane komponenty z klasy ToolBox'''
    def __init__(self, master, controller):
        super().__init__(master, bg="white")
        self.controller = controller

        #Stara płaska struktura self.widgets = []  # Wszystkie dodane widgety
        self._name = "Workspace"
        self.root_node = WidgetNode(self)  # Workspace jako korzeń
        self.selected_widget = None  # Aktualnie zaznaczony widget
        self._group_vars = {}  # Zmienne grupowe dla Radiobuttonów
        self.containers = [self]  # Lista kontenerów (Workspace + Frame/LabelFrame)

        # Konfiguracja siatki
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # @property
    # def _name(self):
    #     return self._name
    #
    # @_name.setter
    # def _name(self, var):
    #     self._name = var

    def widget_initial_set(self, widget, column, row, parent_name):
        widget.controller = self.controller
        widget.row = row
        widget.column = column
        widget.rowspan = 1
        widget.columnspan = 1
        widget.sticky = ""
        widget._parent_name = parent_name

    def add_widget(self, widget_type, parent_name="Workspace"):
        '''Dodaje nowy widget do Workspace'''

        widget = None
        if widget_type == "Label":
            widget = tk.Label(self, text="Nowy Label", bg="lightyellow")

        elif widget_type == "Button":
            widget = tk.Button(self, text="Nowy Button")

        elif widget_type == "Entry":
            widget = tk.Entry(self)

        elif widget_type == "Checkbutton":
            var = tk.BooleanVar(value=False)
            widget = tk.Checkbutton(self, text="Opcja", variable=var)
            widget._linked_var = var

        elif widget_type == "Radiobutton":
            widget = tk.Radiobutton(self, text="Opcja", value="Opcja")
            widget._linked_var = tk.StringVar()
            widget.config(variable=widget._linked_var)

        elif widget_type == "Frame":
            widget = tk.Frame(master=self, bg="lightgray", bd=2, relief="groove", width=200, height=100)
            widget.pack_propagate(False)
            widget._name = f"Frame_{len(self.containers)}"
            self.containers.append(widget)

        elif widget_type == "LabelFrame":
            widget = tk.LabelFrame(master=self, text="Grupa", bg="lightgray", bd=2, relief="ridge", width=200, height=100)
            widget.pack_propagate(False)
            widget._name = f"LabelFrame_{len(self.containers)}"
            self.containers.append(widget)

        else:
            return  # Nieobsługiwany typ

        # Ustawienia początkowe
        # self.widget_initial_set(widget, column=len(self.widgets), row=0)
        self.widget_initial_set(widget, column=0, row=0, parent_name=parent_name)

        # Dodanie do siatki
        widget.grid(column=widget.column, row=widget.row)

        # Obsługa kliknięcia
        widget.bind("<Button-1>", lambda e, w=widget: self.select_widget(w))

        # Dodanie do listy
        #Stara płaska struktura self.widgets.append(widget)
        parent_node = self.find_node_by_name(parent_name)
        new_node = WidgetNode(widget, parent=parent_node)
        parent_node.children.append(new_node)

        # Dodanie do drzewka
        self.controller.tree_panel.add_widget(widget)
        # self.next_column +=1

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
                # Jeśli to kontener → odbuduj gałąź
                if hasattr(self.selected_widget, "_name"):
                    self.controller.tree_panel.rebuild_container_branch(self.selected_widget)
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
        #--new lines 1 --
        node = self.find_node_by_widget(widget)
        old_parent = node.parent
        old_parent.children.remove(node)

        new_parent = self.find_node_by_name(parent_name)
        node.parent = new_parent
        new_parent.children.append(node)

        parent_widget = self.get_parent_container(parent_name)
        widget.grid(column=0, row=0, in_=parent_widget)
        widget._parent_name = parent_name
        widget.grid(
            column=widget.column,
            row=widget.row,
            rowspan=widget.rowspan,
            columnspan=widget.columnspan,
            sticky=widget.sticky
        )

        # Aktualizacja drzewka
        self.controller.tree_panel.rebuild_tree()

    def find_node_by_name(self, name, node=None):
        if node is None:
            node = self.root_node

        widget = node.widget
        widget_name = getattr(widget, "_name", None)
        if widget_name == name or (widget_name is None and name == "Workspace"):
            return node

        for child in node.children:
            result = self.find_node_by_name(name, child)
            if result:
                return result
        return None

    def iter_nodes(self, node=None):
        if node is None:
            node = self.root_node
        yield node
        for child in node.children:
            yield from self.iter_nodes(child)

    def find_node_by_widget(self, widget, node=None):
        '''Znajduje węzeł WidgetNode na podstawie obiektu widget'''
        if node is None:
            node = self.root_node

        if node.widget == widget:
            return node

        for child in node.children:
            result = self.find_node_by_widget(widget, child)
            if result:
                return result
        return None



