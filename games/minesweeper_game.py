import tkinter as tk
import random

class Minesweeper:
    def __init__(self, root, size=8, num_mines=10):
        self.root = root
        self.size = size
        self.num_mines = num_mines
        self.buttons = []
        self.mine_positions = set()
        self.flags = set()  # Conjunto para armazenar posições das bandeiras
        self.revealed_cells = set()  # Conjunto para rastrear as células reveladas

        # Configuração inicial do tabuleiro
        self.create_game_board()

    # Configura ou reinicia o tabuleiro
    def create_game_board(self):
        # Remove componentes antigos do tabuleiro (se existirem)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Cria o tabuleiro e adiciona o botão de reiniciar
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.mine_positions.clear()
        self.flags.clear()
        self.revealed_cells.clear()
        self.place_mines()
        self.calculate_adjacent_mines()
        self.create_buttons()
        
        # Botão para reiniciar o jogo
        restart_button = tk.Button(self.root, text="Reiniciar Jogo", command=self.create_game_board)
        restart_button.grid(row=self.size, column=0, columnspan=self.size)

    # Passo 1: Colocar as minas aleatoriamente
    def place_mines(self):
        while len(self.mine_positions) < self.num_mines:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (row, col) not in self.mine_positions:
                self.mine_positions.add((row, col))
                self.board[row][col] = '💣'  # Emoji de bomba

    # Passo 2: Calcular o número de minas adjacentes
    def calculate_adjacent_mines(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != '💣':
                    count = 0
                    for r in range(max(0, row - 1), min(self.size, row + 2)):
                        for c in range(max(0, col - 1), min(self.size, col + 2)):
                            if (r, c) in self.mine_positions:
                                count += 1
                    self.board[row][col] = str(count) if count > 0 else ' '

    # Passo 3: Revelar célula
    def reveal_cell(self, row, col):
        if (row, col) in self.flags:
            return  # Impede revelar células marcadas com bandeiras

        if (row, col) in self.revealed_cells:
            return  # Impede revelar células já reveladas

        # Revela a célula
        self.revealed_cells.add((row, col))
        if self.board[row][col] == '💣':
            self.buttons[row][col].config(text='💣', bg='red')
            self.game_over(False)
        elif self.board[row][col] == ' ':
            self.buttons[row][col].config(text=' ', bg='lightgrey', state='disabled')
            self.reveal_adjacent_cells(row, col)
        else:
            self.buttons[row][col].config(text=self.board[row][col], bg='lightgrey', state='disabled')

        # Verifica se o jogador ganhou
        if self.check_win():
            self.game_over(True)

    # Função para colocar ou remover uma bandeira com o botão direito
    def toggle_flag(self, row, col, event):
        if self.buttons[row][col]['state'] == 'disabled':
            return  # Impede marcar células já reveladas

        if (row, col) in self.flags:
            # Remove bandeira
            self.buttons[row][col].config(text='', fg='black')
            self.flags.remove((row, col))
        else:
            # Coloca bandeira
            self.buttons[row][col].config(text='🚩', fg='red')
            self.flags.add((row, col))

    # Função para revelar células adjacentes se não houver minas ao redor
    def reveal_adjacent_cells(self, row, col):
        for r in range(max(0, row - 1), min(self.size, row + 2)):
            for c in range(max(0, col - 1), min(self.size, col + 2)):
                if self.buttons[r][c]['state'] == 'normal' and (r, c) not in self.flags:
                    self.reveal_cell(r, c)

    # Função para criar os botões na interface gráfica
    def create_buttons(self):
        self.buttons = []
        for row in range(self.size):
            button_row = []
            for col in range(self.size):
                button = tk.Button(self.root, width=2, height=1, command=lambda r=row, c=col: self.reveal_cell(r, c))
                button.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(r, c, event))  # Clique direito
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    # Função para verificar se o jogador ganhou
    def check_win(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != '💣' and self.buttons[row][col]['state'] == 'normal':
                    return False
        return True

    # Função para terminar o jogo
    def game_over(self, won):
        # Revela todas as minas e desativa os botões
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == '💣':
                    self.buttons[row][col].config(text='💣', bg='red')
                # Desativa todos os botões
                self.buttons[row][col].config(state='disabled')
        
        result_text = "Parabéns, você ganhou!" if won else "BOOM! Você perdeu."
        result_label = tk.Label(self.root, text=result_text, font=('Arial', 12))
        result_label.grid(row=self.size + 1, column=0, columnspan=self.size)

# Inicia a janela do Tkinter
root = tk.Tk()
root.title("Campo Minado")
game = Minesweeper(root)
root.mainloop()