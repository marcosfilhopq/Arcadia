import tkinter as tk
import random

class Minesweeper:
    def __init__(self, root, size=8, num_mines=10):
        self.root = root
        self.size = size
        self.num_mines = num_mines
        self.buttons = []
        self.mine_positions = set()
        self.flags = set()
        self.revealed_cells = set()
        self.create_game_board()

    def create_game_board(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.mine_positions.clear()
        self.flags.clear()
        self.revealed_cells.clear()
        self.place_mines()
        self.calculate_adjacent_mines()
        self.create_buttons()

        restart_button = tk.Button(self.root, text="Reiniciar Jogo", command=self.create_game_board)
        restart_button.grid(row=self.size, column=0, columnspan=self.size)

    def place_mines(self):
        while len(self.mine_positions) < self.num_mines:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (row, col) not in self.mine_positions:
                self.mine_positions.add((row, col))
                self.board[row][col] = '💣'

    def calculate_adjacent_mines(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != '💣':
                    count = sum((r, c) in self.mine_positions for r in range(max(0, row - 1), min(self.size, row + 2))
                                for c in range(max(0, col - 1), min(self.size, col + 2)))
                    self.board[row][col] = str(count) if count > 0 else ' '

    def reveal_cell(self, row, col):
        if (row, col) in self.flags or (row, col) in self.revealed_cells:
            return

        self.revealed_cells.add((row, col))
        if self.board[row][col] == '💣':
            self.buttons[row][col].config(text='💣', bg='red')
            self.game_over(False)
        elif self.board[row][col] == ' ':
            self.buttons[row][col].config(text=' ', bg='lightgrey', state='disabled')
            self.reveal_adjacent_cells(row, col)
        else:
            self.buttons[row][col].config(text=self.board[row][col], bg='lightgrey', state='disabled')

        if self.check_win():
            self.game_over(True)

    def toggle_flag(self, row, col, event):
        if self.buttons[row][col]['state'] == 'disabled':
            return

        if (row, col) in self.flags:
            self.buttons[row][col].config(text='', fg='black')
            self.flags.remove((row, col))
        else:
            self.buttons[row][col].config(text='🚩', fg='red')
            self.flags.add((row, col))

    def reveal_adjacent_cells(self, row, col):
        for r in range(max(0, row - 1), min(self.size, row + 2)):
            for c in range(max(0, col - 1), min(self.size, col + 2)):
                if self.buttons[r][c]['state'] == 'normal' and (r, c) not in self.flags:
                    self.reveal_cell(r, c)

    def create_buttons(self):
        self.buttons = []
        for row in range(self.size):
            button_row = []
            for col in range(self.size):
                button = tk.Button(self.root, width=2, height=1, command=lambda r=row, c=col: self.reveal_cell(r, c))
                button.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c, event))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def check_win(self):
        return all(self.board[row][col] == '💣' or self.buttons[row][col]['state'] == 'disabled'
                   for row in range(self.size) for col in range(self.size))

    def game_over(self, won):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == '💣':
                    self.buttons[row][col].config(text='💣', bg='red')
                self.buttons[row][col].config(state='disabled')

        result_text = "Parabéns, você ganhou!" if won else "BOOM! Você perdeu."
        result_label = tk.Label(self.root, text=result_text, font=('Arial', 12))
        result_label.grid(row=self.size + 1, column=0, columnspan=self.size)
