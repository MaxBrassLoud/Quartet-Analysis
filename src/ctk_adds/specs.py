import customtkinter as ctk

class CarSpecsTable(ctk.CTkFrame):
    def __init__(self, master, float_column_name: str = "Bewertung", **kwargs):
        super().__init__(master, **kwargs)

        self.float_column_name = float_column_name
        self.car_name = None
        self.specs = None
        self.floats = None

        self.widgets = []  # für dynamisches Löschen
        self.title_label = None

    def set_specs(self, specs_dict: dict):
        if not specs_dict or len(specs_dict) != 1:
            self._clear_table()
            return

        self.car_name = list(specs_dict.keys())[0]
        self.specs = specs_dict[self.car_name]
        self._try_render()

    def set_floats(self, float_dict: dict):
        self.floats = float_dict
        self._try_render()

    def _try_render(self):
        if self.specs is not None and self.floats is not None:
            self._render_table()
        else:
            self._clear_table()

    def _clear_table(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        if self.title_label:
            self.title_label.destroy()
            self.title_label = None

    def _render_table(self):
        self._clear_table()

        # Title
        self.title_label = ctk.CTkLabel(self, text=self.car_name, font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(10, 10))
        self.widgets.append(self.title_label)

        # Header
        headers = ["Kategorie", "Wert", self.float_column_name]
        for col, header in enumerate(headers):
            lbl = ctk.CTkLabel(self, text=header, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=1, column=col, padx=10, pady=5, sticky="w")
            self.widgets.append(lbl)

        # Rows
        for row_idx, (key, value) in enumerate(self.specs.items(), start=2):
            float_val = self.floats.get(key, "—")

            key_lbl = ctk.CTkLabel(self, text=key)
            val_lbl = ctk.CTkLabel(self, text=value)
            float_lbl = ctk.CTkLabel(self, text=str(float_val))

            key_lbl.grid(row=row_idx, column=0, padx=10, pady=2, sticky="w")
            val_lbl.grid(row=row_idx, column=1, padx=10, pady=2, sticky="w")
            float_lbl.grid(row=row_idx, column=2, padx=10, pady=2, sticky="w")

            self.widgets.extend([key_lbl, val_lbl, float_lbl])


if __name__ == "__main__":
    import tkinter as tk

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("500x400")

    table = CarSpecsTable(root, float_column_name="Score")
    table.pack(padx=20, pady=20, fill="both", expand=True)

    # Erst nur Bewertungen setzen → kein Output
    table.set_floats({
        "kmh": 9.8,
        "kg": 7.1,
        "ps": 9.5,
        "ccm": 8.0,
        "pistons": 7.2,
        "rpm": 9.1
    })

    # Jetzt Specs setzen → Tabelle wird angezeigt
    table.set_specs({
        "Lamborghini Aventador": {
            "kmh": "349",
            "kg": "1575",
            "ps": "700",
            "ccm": "6498",
            "pistons": "12",
            "rpm": "8250"
        }
    })

    root.mainloop()
