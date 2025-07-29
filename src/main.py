import json
import customtkinter as ctk
import ctk_adds.Shortcut_Input as ip
import ctk_adds.specs as specs
import logging
from tkinter import filedialog as fd
from tkinter import messagebox as mg

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename=".log")






class UI_Actions:
    def __init__(self):
        self.filename:str = None
    def openFile(self):
        
        temp_filename = fd.askopenfile(filetypes=[(".json", "json Dateien")])
        if temp_filename:
            self.filename = temp_filename.name


    def start(self, other, another):
        if self.filename == None:
            mg.showwarning("Warnung", "Bitte wähle eine Gültige Datei aus!")
        else:
            another.havedata(another.open_file(filepath=self.filename))
            other.start_frame.pack_forget()
            other.mainframe()

class Backend:
    def __init__(self):

        self.MyCards:list = []
        self.oponentcards:list = []
        self.shortcuts:json = None
        self.file_path:str = None
        self.data:json = None
        self.temp_card:str = None

    def open_file(self, filepath) -> json:
        self.file_path = filepath
        with open(filepath, "r") as f:
            data = f.read()
            data = json.loads(data)
            self.data = data
            return data
        
    def havedata(self, data:json):
        self.shortcuts = data["shortcuts"]

        


    def AddMyCard(self, shortcut, other):
        """Fügt eine Karte zu MyCards hinzu, wenn sie beim Gegner war."""
        if self.CheckShortcut(shortcut):
            logging.info(f"Won Shortcut: {shortcut}")
            other.input.clear()
            try:
                if shortcut not in self.MyCards:
                    self.MyCards.append(shortcut)

                if shortcut in self.oponentcards:
                    self.oponentcards.remove(shortcut)
            finally:
                logging.info(f"MyCards: {self.MyCards}")
                logging.info(f"OponentCards: {self.oponentcards}")


    def LostCard(self, shortcut, other):
        """Entfernt eine Karte aus MyCards und fügt sie dem Gegner hinzu."""
        if self.CheckShortcut(shortcut):
            logging.info(f"Lost Shortcut: {shortcut}")
            other.input.clear()
            try:
                if shortcut in self.MyCards:
                    self.MyCards.remove(shortcut)

                if shortcut not in self.oponentcards:
                    self.oponentcards.append(shortcut)
            finally:
                logging.info(f"MyCards: {self.MyCards}")
                logging.info(f"OponentCards: {self.oponentcards}")

    
    def CheckShortcut(self, shortcut):
        if shortcut in self.shortcuts:
            return True
        else:
            return False
        
    def startEval(self, shortcut, UI):
        self.temp_card = shortcut
        if self.CheckShortcut(shortcut):
            UI.specsTable.set_floats(self.get_car_scores(shortcut))
            UI.specsTable.set_specs(self.get_car_stats(shortcut))
            UI.LabelBest.configure(text=f"Die beste Kategorie für diese Karte ist: {self.bewertung(shortcut=shortcut)}")

    def parse_values(self, car_stats):
        return {k: int(v) for k, v in car_stats.items()}

    def bewertung(self, shortcut):
        data = self.data
        structure = data["structure"]["element_name"]
        shortcuts = data["shortcuts"]
        content = data["content"]

        if shortcut not in shortcuts:
            return f"Ungültiges Kürzel: {shortcut}"

        name = shortcuts[shortcut]
        if name not in content:
            return f"Element nicht gefunden: {name}"

        this_car = self.parse_values(content[name])
        scores = {cat_data["cat"]: 0 for cat_data in structure.values()}

        for other_name, other_data in content.items():
            other_shortcut = next((k for k, v in shortcuts.items() if v == other_name), None)
            if other_name == name or other_shortcut in self.MyCards:
                continue

            other_car = self.parse_values(other_data)

            for cat_key, cat_data in structure.items():
                cat = cat_data["cat"]
                order = cat_data["order"]
                a = this_car[cat]
                b = other_car[cat]

                if order == "<=":
                    scores[cat] += 1 if a > b else -1 if a < b else +0.5
                elif order == ">=":
                    scores[cat] += 1 if a < b else -1 if a > b else +0.5

        beste_kat = max(scores.items(), key=lambda x: x[1])
        print(beste_kat[0])
        beste_kat = self.data["nicer_names_cats"][beste_kat[0]]
        print(beste_kat)
        return beste_kat

    
    def get_car_stats(self, shortcut: str) -> dict:
        data = self.data
        content = data["content"]
        shortcuts = data["shortcuts"]

        if shortcut not in shortcuts:
            raise ValueError(f"Ungültiges Kürzel: {shortcut}")

        name = shortcuts[shortcut]
        if name not in content:
            raise ValueError(f"Element nicht gefunden: {name}")

        return {name: content[name]}



    def get_car_scores(self, shortcut: str) -> dict:
        data = self.data
        structure = data["structure"]["element_name"]
        shortcuts = data["shortcuts"]
        content = data["content"]

        if shortcut not in shortcuts:
            raise ValueError(f"Ungültiges Kürzel: {shortcut}")

        name = shortcuts[shortcut]
        if name not in content:
            raise ValueError(f"Element nicht gefunden: {name}")

        this_car = self.parse_values(content[name])
        scores = {cat_data["cat"]: 0 for cat_data in structure.values()}

        for other_name, other_data in content.items():
            other_shortcut = next((k for k, v in shortcuts.items() if v == other_name), None)
            if other_name == name or other_shortcut in self.MyCards:
                continue

            other_car = self.parse_values(other_data)

            for cat_key, cat_data in structure.items():
                cat = cat_data["cat"]
                order = cat_data["order"]
                a = this_car[cat]
                b = other_car[cat]

                if order == "<=":
                    scores[cat] += 1 if a > b else -1 if a < b else 0.5
                elif order == ">=":
                    scores[cat] += 1 if a < b else -1 if a > b else 0.5

        return scores



# Beispiel
class UI:
    def __init__(self):
        self.Be = Backend()
        self.UI_be = UI_Actions()

        self.app = ctk.CTk()

        self.app.geometry("500x500")

        self.app.title("Quartet Hacks")
    def startframe(self):
        self.start_frame = ctk.CTkFrame(self.app)
        self.start_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.file_choose_label = ctk.CTkLabel(self.start_frame, text="Bitte wähle eine Datei aus welche eine Liste aller aller \n Karten des Spieles enthält siehe in der Dokumentation nach in welchem \n Format diese .json Datei aufgebaut sein muss!")
        self.file_choose_label.pack(padx="10", pady="25")

        self.file_choose_button = ctk.CTkButton(self.start_frame, text="Datei auswählen", command=lambda: self.UI_be.openFile())
        self.file_choose_button.pack(padx="10", pady="25")

        self.StartGameButton = ctk.CTkButton(self.start_frame, text="Start the application", command=lambda: self.UI_be.start(other=self, another=self.Be))
        self.StartGameButton.pack(padx="10", pady="25")

    def mainframe(self):
        self.main_Frame = ctk.CTkScrollableFrame(self.app)
        self.main_Frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.input = ip.ShortcutEntry(self.main_Frame, title="Shortcuts")
        self.input.pack()
        self.ev = ctk.CTkButton(self.main_Frame, text="Evaluate", command=lambda: Backend.startEval(self.Be, self.input.get_value(), self))
        self.ev.pack()
        
        self.specsTable = specs.CarSpecsTable(self.main_Frame)
        self.specsTable.pack()

        self.LabelBest = ctk.CTkLabel(self.main_Frame, text="")
        self.LabelBest.pack(padx="10", pady="25")

        self.buttonlost = ctk.CTkButton(self.main_Frame, text="Karte Verloren", command=lambda: self.Be.LostCard(self.input.get_value(),self))
        self.buttonlost.pack()#.grid(row=1, column=1, padx=5, pady=10)

        self.buttonwon = ctk.CTkButton(self.main_Frame, text="Karte Gewonnen", command=lambda: self.Be.AddMyCard(self.input.get_value(), self))
        self.buttonwon.pack()#.grid(row=1, column=2, padx=5, pady=10)

        

    def mainloop(self):
        self.app.mainloop()
    
if __name__ == "__main__":
    app = UI()
    app.startframe()

    app.mainloop()