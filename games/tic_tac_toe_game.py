import tkinter as tk

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha")
        self.current_player = "X"
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_buttons()
        self.result_label = tk.Label(self.root, text="", font=('Arial', 12))
        self.result_label.grid(row=3, column=0, columnspan=3)

    def create_buttons(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text=" ", width=5, height=2,
                                   command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner(self.current_player):
                self.result_label.config(text=f"Parabéns! O jogador {self.current_player} venceu!")
                self.disable_buttons()
            elif self.is_board_full():
                self.result_label.config(text="O jogo terminou em empate!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
        # Checa linhas, colunas e diagonais
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    def is_board_full(self):
        return all([cell != " " for row in self.board for cell in row])

    def disable_buttons(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(state="disabled")

def start_tic_tac_toe():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()