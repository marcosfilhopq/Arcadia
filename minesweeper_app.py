import sys
from minesweeper_game import Minesweeper  # Agora importa corretamente
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Garante que a pasta do script está no path

import tkinter as tk
from minesweeper_game import Minesweeper  # Agora deve funcionar

def iniciar_jogo():
    root = tk.Tk()
    root.title("Campo Minado")
    game = Minesweeper(root)
    root.mainloop()

if __name__ == '__main__':
    iniciar_jogo()
