import tkinter as tk
from tkinter import ttk

class WidgetTreePanel(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Dodaj korzeń
        self.root_id = self.tree.insert("", "end", text="Workspace", open=True)

    def add_widget(self, widget):
        parent_name = getattr(widget, "_parent_name", "Workspace")
        parent_id = self.find_tree_id(parent_name)
        if not parent_id:
            print(f"[WARN] Nie znaleziono rodzica '{parent_name}' w drzewku. Dodaję do Workspace.")
            parent_id = self.root_id  # fallback

        # Jeśli to kontener — dodaj jako gałąź
        if isinstance(widget, (tk.Frame, tk.LabelFrame)):
            widget_id = self.tree.insert(parent_id, "end", text=widget._name, open=True)
        else:
            widget_id = self.tree.insert(parent_id, "end", text=widget.winfo_class())

        widget._tree_id = widget_id

    def find_tree_id(self, name):
        def recursive_search(parent):
            for item in self.tree.get_children(parent):
                if self.tree.item(item, "text") == name:
                    return item
                result = recursive_search(item)
                if result:
                    return result
            return None

        # Jeśli szukamy Workspace
        if name == "Workspace":
            return getattr(self, "root_id", None)

        result = recursive_search(getattr(self, "root_id", ""))
        return result

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return  # nic nie zaznaczono → wyjście

        selected_id = selection[0]
        for node in self.controller.workspace.iter_nodes():
            widget = node.widget
            if getattr(widget, "_tree_id", None) == selected_id:
                self.controller.workspace.select_widget(widget)
                self.controller.properties.display_properties(widget)
                break

    def move_widget(self, widget):
        '''Przenosi widget w drzewku do nowego kontenera'''
        # Usuń stare wpisy
        old_id = getattr(widget, "_tree_id", None)
        if old_id:
            self.tree.delete(old_id)

        # Znajdź nowego rodzica
        parent_name = getattr(widget, "_parent_name", "Workspace")
        parent_id = self.find_tree_id(parent_name)

        # Dodaj ponownie widget pod nowym rodzicem
        new_id = self.tree.insert(parent_id, "end", text=widget.winfo_class())
        widget._tree_id = new_id

    def rebuild_container_branch(self, container_widget):
        '''Odbudowuje gałąź kontenera i jego dzieci w drzewku'''
        # Usuń starą gałąź
        old_id = getattr(container_widget, "_tree_id", None)
        if old_id:
            self.tree.delete(old_id)

        # Znajdź nowego rodzica
        parent_name = getattr(container_widget, "_parent_name", "Workspace")
        parent_id = self.find_tree_id(parent_name)

        # Dodaj kontener jako gałąź
        new_id = self.tree.insert(parent_id, "end", text=container_widget._name, open=True)
        container_widget._tree_id = new_id

        # Dodaj dzieci kontenera
        for widget in self.controller.workspace.widgets:
            if getattr(widget, "_parent_name", "Workspace") == container_widget._name:
                child_id = self.tree.insert(new_id, "end", text=widget.winfo_class())
                widget._tree_id = child_id

    def build_tree(self, node, parent_id=""):
        widget = node.widget
        label = getattr(widget, "_name", widget.winfo_class())
        node_id = self.tree.insert(parent_id, "end", text=label, open=True)
        widget._tree_id = node_id

        for child in node.children:
            self.build_tree(child, node_id)

    def rebuild_tree(self):
        '''Czyści i buduje drzewko od nowa na podstawie struktury WidgetNode'''
        self.tree.delete(*self.tree.get_children())
        self.build_tree(self.controller.workspace.root_node)
