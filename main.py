import tkinter as tk
from src.functions import QuizApp
from src.player import Player

def main():
    player_1 = Player()

    root = tk.Tk()
    app = QuizApp(root)

    root.mainloop()

        
if __name__ == "__main__":
    main()