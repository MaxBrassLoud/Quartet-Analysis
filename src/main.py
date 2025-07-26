import json
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mg

def open_file(file_name) -> json:
    with open(file_name, "r") as f:
        data = f.read()
        data = json.loads(data)
        return data

def parse_values(car_stats):
    return {k: int(v) for k, v in car_stats.items()}

def bewertung(shortcut, data:json):

    # Zugriff auf strukturierte Daten
    
    structure = data["structure"]["element_name"]
    shortcuts = data["shortcuts"]
    content = data["content"]
    if shortcut not in shortcuts:
        return f"Ungültiges Kürzel: {shortcut}"
    
    name = shortcuts[shortcut]
    if not name in content:
        return f"Element nicht gefunden: {name} "
    
    this_car = parse_values(content[name])
    scores = {cat_data["cat"]: 0 for cat_data in structure.values()}

    for other_name, other_data in content.items():
        if other_name == name:
            continue
        other_car = parse_values(other_data)

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

    print(f"\nBewertung für: {name} ({shortcut})")
    for cat, score in scores.items():
        print(f"  {cat}: {float(score)}")
    print(f"\n➡️  Beste Kategorie: {beste_kat[0]} (Score: {beste_kat[1]})")
    return beste_kat
class AppActions:
    def __init__(self):
        self.filename:str = None
    def openFile(self):
        
        temp_filename = fd.askopenfile(filetypes=[(".json", "json Dateien")])
        if temp_filename:
            self.filename = temp_filename.name


    def start(self):
        if self.filename == None:
            mg.showwarning("Warnung", "Bitte wähle eine Gültige Datei aus!")
        else:
            start_frame.pack_forget()
            main_Frame.pack()

class CarDB:
    def __init__(self, data:json):

        self.myCars:list = []
        self.oponentcars:list = []
        self.shortcuts = data["shortcuts"]
        
        
    def AddMyCar(self, shortcut):
        
        if self.CheckShortcut(shortcut):
            self.myCars.append(shortcut)
        else:
            raise SyntaxError(f"Invalid Syntax for {shortcut}")
    def CheckShortcut(self, shortcut):
        if shortcut in self.shortcuts:
            return True
        else:
            return False
# Beispiel

app_backend = AppActions()

app = tk.Tk()

app.title("Quartet Strategie")
start_frame = tk.Frame(app)
start_frame.pack()

file_choose_label = tk.Label(start_frame, text="Bitte wähle eine Datei aus welche eine Liste aller aller \n Karten des Spieles enthält siehe in der Dokumentation nach in welchem \n Format diese .json Datei aufgebaut sein muss!")
file_choose_label.pack()

file_choose_button = tk.Button(start_frame, text="Datei auswählen", command=lambda: app_backend.openFile())
file_choose_button.pack()

StartGameButton = tk.Button(start_frame, text="Start the application", command=lambda: app_backend.start())
StartGameButton.pack(padx="10", pady="25")



main_Frame = tk.Frame(app)


app.mainloop()

# if __name__ == "__main__":
#     data = open_file("src/data/cars.json")
#     start = CarDB(data=data)
#     # data = open_file("cars.json")
#     # while True:
#     #     const = input("\n >> ")
#     #     if const == "end":
#     #         print("game ended")
#     #     else:
#     #         bt, ct = bewertung(const, data )
#     #         print(f"Die beste Kategorie ist {bt} mit einem wert von {ct}")