# ♠️ Quartet Analysis App

**Strategic. Fast. Simple.**  
The **Quartet Analysis App** helps you analyze and manage your card deck to improve your strategy in quartet-style games. Use it to evaluate your moves, optimize your deck, and keep track of won or lost cards during gameplay.

---

## 🚀 Features

- 🗂 **Import your own card deck** via a `.json` file  
- 📊 **Automatically evaluate cards** – find the best category to play  
- ✅ **Track won and lost cards** dynamically during the game  
- 🔍 **Compare your cards against remaining ones in the deck**  
- 💡 **User-friendly GUI built with CustomTkinter**

---


## 📁 JSON File Structure

To work correctly, the app requires a `.json` file containing your full card deck and rules.

An example file is located at:

```text
/data/template.json
```
It should have the following structure:
```json
{
  "structure": {
    "element_name": {
      "horsepower": { "cat": "PS", "order": ">=" },
      "speed": { "cat": "kmh", "order": ">=" }
    }
  },
  "shortcuts": {
    "a1": "BMW M3",
    "b2": "Audi RS6"
  },
  "content": {
    "BMW M3": { "PS": "431", "kmh": "250" },
    "Audi RS6": { "PS": "600", "kmh": "305" }
  },
  "nicer_names_cats": {
    "PS": "Horsepower",
    "kmh": "Top Speed"
  }
}
```
 - structure: Defines categories and how they should be compared (>= or <=)

 - shortcuts: Maps card codes to their full names

 - content: Holds the actual stats for each card

 - nicer_names_cats: Human-readable labels for category names

## 🛠️ Installation
1. Install dependencies

```bach
pip install customtkinter
```

2. Clone the repository

```bash#
git clone https://github.com/MaxBrassLoud/Quartet-Analysis.git
cd Quartet-Analysis
```

3. Start the application

```bash
python main.py
```

--

## ✅ How to Use

1. Launch the app.

2. Choose a .json file containing your full deck.

3. Enter the shortcut (e.g. a1, b2, etc.) of your current card.

4. Use the buttons to:

  - Evaluate: Analyze the card and find its strongest category.

  - Card Won: Add this card to your collection.

  - Card Lost: Mark this card as lost and assign it to the opponent.

All actions are processed locally – no data is sent externally.

## 🧠 Evaluation Logic
The app compares the selected card to all other cards (excluding your own).
It calculates scores for each category based on the comparison rules defined in the JSON (>= or <=) and identifies the best category to play for maximum advantage.

## 📄 License
This project is licensed under the MIT License – you are free to use, modify, and distribute it.

## 👤 Author
MaxBrassLoud
🔗 &nbsp;[View GitHub Profile](https://github.com/MaxBrassLoud)

