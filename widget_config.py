# widget_config.py

import tkinter as tk

WIDGET_PROPERTIES = {
    "Common": {
        "Parent": {
            "type": "dropdown",
            "getter": lambda w: getattr(w, "_parent_name", "Workspace"),
            "setter": lambda w, v: w.controller.workspace.reparent_widget(w, v),
            "options": lambda w: [getattr(c, "_name", "Workspace") for c in w.controller.workspace.containers]
        },
        "row": {
            "type": "entry",
            "getter": lambda w: w.grid_info()["row"],
            "setter": lambda w, v: w.grid_configure(row=int(v))
        },
        "column": {
            "type": "entry",
            "getter": lambda w: w.grid_info()["column"],
            "setter": lambda w, v: w.grid_configure(column=int(v))
        },
        "rowspan": {
            "type": "entry",
            "getter": lambda w: w.grid_info()["rowspan"],
            "setter": lambda w, v: w.grid_configure(rowspan=int(v))
        },
        "columnspan": {
            "type": "entry",
            "getter": lambda w: w.grid_info()["columnspan"],
            "setter": lambda w, v: w.grid_configure(columnspan=int(v))
        },
        "sticky": {
            "type": "entry",
            "getter": lambda w: w.grid_info()["sticky"],
            "setter": lambda w, v: w.grid_configure(sticky=v)
        }
    },
    "Label": {
        "text": {"type": "entry", "getter": lambda w: w.cget("text"), "setter": lambda w, v: w.config(text=v)},
        "bg": {"type": "entry", "getter": lambda w: w.cget("bg"), "setter": lambda w, v: w.config(bg=v)}
    },
    "Button": {
        "text": {"type": "entry", "getter": lambda w: w.cget("text"), "setter": lambda w, v: w.config(text=v)},
        "fg": {"type": "entry", "getter": lambda w: w.cget("fg"), "setter": lambda w, v: w.config(fg=v)}

    },
    "Entry": {
        "value": {"type": "entry", "getter": lambda w: w.get(),
                  "setter": lambda w, v: (w.delete(0, tk.END), w.insert(0, v))}
    },
    "Checkbutton": {
        "text": {
            "type": "entry",
            "getter": lambda w: w.cget("text"),
            "setter": lambda w, v: w.config(text=v)
        },
        "value": {
            "type": "checkbox",
            "getter": lambda w: w._linked_var.get(),
            "setter": lambda w, v: w._linked_var.set(bool(int(v)))
        }
    },
    "Frame": {
        "width": {
            "type": "entry",
            "getter": lambda w: w.winfo_width(),
            "setter": lambda w, v: w.config(width=int(v))
        },
        "height": {
            "type": "entry",
            "getter": lambda w: w.winfo_height(),
            "setter": lambda w, v: w.config(height=int(v))
        }
    },
    "Radiobutton": {
        "text": {
            "type": "entry",
            "getter": lambda w: w.cget("text"),
            "setter": lambda w, v: w.config(text=v)
        },
        "value": {
            "type": "entry",
            "getter": lambda w: w.cget("value"),
            "setter": lambda w, v: w.config(value=v)
        },
        "group": {
            "type": "entry",
            "getter": lambda w: getattr(w._linked_var, "name", ""),
            "setter": lambda w, v: w.controller.workspace.assign_group_variable(w, v)
        }
    },
    # "Parent": {
    #     "type": "dropdown",
    #     "getter": lambda w: getattr(w, "_parent_name", "Workspace"),
    #     "setter": lambda w, v: w.controller.workspace.reparent_widget(w, v),
    #     "options": lambda w: [getattr(c, "_name", "Workspace") for c in w.controller.workspace.containers]
    # },
    "LabelFrame": {
        "text": {
            "type": "entry",
            "getter": lambda w: w.cget("text"),
            "setter": lambda w, v: w.config(text=v)
        },
        "width": {
            "type": "entry",
            "getter": lambda w: w.winfo_width(),
            "setter": lambda w, v: w.config(width=int(v))
        },
        "height": {
            "type": "entry",
            "getter": lambda w: w.winfo_height(),
            "setter": lambda w, v: w.config(height=int(v))
        }
    }

}
