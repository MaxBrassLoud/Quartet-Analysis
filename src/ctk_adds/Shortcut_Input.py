

import customtkinter as ctk

class ShortcutEntry(ctk.CTkFrame):
    def __init__(self, master, FirstP:list=["A", "B", "C", "D", "E", "F", "G", "H"] , SecondP:list=["1","2","3","4"] ,title=None,  *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.entries = []
        self.P1 = FirstP
        self.P2 = SecondP
        
        # Optionaler Titel
        if title:
            self.label = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=18, weight="bold"))
            self.label.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        # Eingabefelder
        for i in range(2):
            entry = ctk.CTkEntry(self, width=40, justify='center', font=ctk.CTkFont(size=16))
            entry.grid(row=1, column=i, padx=5, pady=10)
            entry.bind("<KeyRelease>", lambda e, idx=i: self._validate_and_focus(e, idx))
            self.entries.append(entry)
    def checkinput(self, input_:str, index:int):
        if index == 0:
            Chars_Set = self.P1
            if input_ not in Chars_Set:
                return True
            else: return False
        elif index == 1:
            Chars_Set2 = self.P2
            if input_ not in Chars_Set2:
                return True
            else: return False
        else:
            raise ValueError("Please Enter only the right numbers")
    def lock(self):
        for entry in self.entries:
            entry.configure(state='disabled')
    
    def unlock(self):
        for entry in self.entries:
            entry.configure(state='normal')
    
    def insert_value(self, value):
        if len(value) != len(self.entries):
            raise ValueError("Value length does not match the number of entries.")
        for entry, char in zip(self.entries, value):
            entry.delete(0, ctk.END)
            entry.insert(0, char)
            entry.configure(state='disabled')

    def _validate_and_focus(self, event, index):
        widget = event.widget
        value = widget.get()

        try:
            if self.checkinput(value, index):
                widget.delete(0, ctk.END)
            elif len(value) > 1:
                widget.delete(1, ctk.END)
            else:
                try:
                    self.entries[index + 1].focus()
                except IndexError:
                    pass                    
    
        except ValueError as e:
            print(e)
            

            

    def get_value(self):
        values = [entry.get() for entry in self.entries]
        if any(v == '' for v in values):
            return False
        return ''.join(values)

    def clear(self):
        for entry in self.entries:
            entry.delete(0, ctk.END)

# Beispielanwendung
if __name__ == "__main__":
    
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Ziffernreihe mit Titel")

    # DigitEntryRow mit Titel
    row = ShortcutEntry(app, title="Shortcut:")
    row.pack(pady=20)

    def show_value():
        print(row.get_value())

    ctk.CTkButton(app, text="Ausgeben", command=show_value).pack(pady=5)
    ctk.CTkButton(app, text="Löschen", command=row.clear).pack(pady=5)

    row.entries[0].focus()
    print(ShortcutEntry.checkinput(self=row, input_=2, index=1))
    app.mainloop()

    
