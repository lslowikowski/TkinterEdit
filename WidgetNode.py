class WidgetNode:
    def __init__(self, widget, parent=None):
        self.widget = widget
        self.parent = parent
        self.children = []