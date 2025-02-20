import tkinter as tk
from tkinter import messagebox
import random

class PedraPapelTesouraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pedra, Papel, Tesoura, Lagarto, Spock")
        self.opcoes = ["Pedra", "Papel", "Tesoura", "Lagarto", "Spock"]
        self.regras = {
            "Pedra": ["Tesoura", "Lagarto"],
            "Papel": ["Pedra", "Spock"],
            "Tesoura": ["Papel", "Lagarto"],
            "Lagarto": ["Spock", "Papel"],
            "Spock": ["Tesoura", "Pedra"]
        }

        # Placar
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0

        # Criar widgets
        self.label = tk.Label(self.root, text="Escolha sua jogada:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.botoes_frame = tk.Frame(self.root)
        self.botoes_frame.pack(pady=10)

        for opcao in self.opcoes:
            botao = tk.Button(self.botoes_frame, text=opcao, font=("Arial", 12), width=12, 
                            command=lambda o=opcao: self.jogar(o))
            botao.pack(side=tk.LEFT, padx=5)

        self.placar_label = tk.Label(self.root, text="Placar: 0 Vitórias, 0 Derrotas, 0 Empates", font=("Arial", 12))
        self.placar_label.pack(pady=10)

        self.historico = []

    def jogar(self, escolha_jogador):
        """Executa uma rodada do jogo."""
        escolha_computador = random.choice(self.opcoes)

        # Determina o resultado
        if escolha_jogador == escolha_computador:
            resultado = "Empate"
            self.empates += 1
        elif escolha_computador in self.regras[escolha_jogador]:
            resultado = "Vitória"
            self.vitorias += 1
        else:
            resultado = "Derrota"
            self.derrotas += 1

        # Atualiza o placar
        self.atualizar_placar()

        # Adiciona ao histórico
        self.historico.append(f"Você: {escolha_jogador}, Computador: {escolha_computador}, Resultado: {resultado}")

        # Mostra o resultado
        messagebox.showinfo("Resultado", f"Você escolheu: {escolha_jogador}\n"
                                        f"Computador escolheu: {escolha_computador}\n"
                                        f"Resultado: {resultado}")

    def atualizar_placar(self):
        """Atualiza o placar na interface."""
        self.placar_label.config(text=f"Placar: {self.vitorias} Vitórias, {self.derrotas} Derrotas, {self.empates} Empates")

    def mostrar_historico(self):
        """Mostra o histórico de partidas."""
        historico_str = "\n".join(self.historico) if self.historico else "Nenhuma partida jogada ainda."
        messagebox.showinfo("Histórico de Partidas", historico_str)

# Configuração da janela principal
if __name__ == "__main__":
    root = tk.Tk()
    app = PedraPapelTesouraGUI(root)

    # Botão para exibir o histórico
    historico_btn = tk.Button(root, text="Exibir Histórico", font=("Arial", 12), command=app.mostrar_historico)
    historico_btn.pack(pady=5)

    root.mainloop()