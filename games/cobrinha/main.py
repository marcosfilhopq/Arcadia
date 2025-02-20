import pygame
import random
import json
from entidade import Entidade
from cobra import Cobra
from comida import Comida
from io import BytesIO
import requests

# Função para carregar e salvar o recorde
def carregar_recorde():
    try:
        with open('recorde.json', 'r') as arquivo:
            dados = json.load(arquivo)
            return dados.get("recorde", 0)
    except FileNotFoundError:
        return 0

def salvar_recorde(recorde):
    with open('recorde.json', 'w') as arquivo:
        json.dump({"recorde": recorde}, arquivo)

def mostrar_tela_fim_de_jogo(tela, pontos, recorde):
    tela.fill((0, 0, 0))

    font = pygame.font.SysFont(None, 48)
    texto_pontos = font.render(f"Pontuação: {pontos}", True, (255, 255, 255))
    tela.blit(texto_pontos, (250, 150))

    # Exibir o recorde
    texto_recorde = font.render(f"Recorde: {recorde}", True, (255, 255, 0))
    tela.blit(texto_recorde, (250, 200))

    font_botao = pygame.font.SysFont(None, 36)
    texto_novo_jogo = font_botao.render("Novo Jogo", True, (0, 255, 0))
    retangulo_novo_jogo = pygame.Rect(225, 250, 150, 50)
    pygame.draw.rect(tela, (255, 255, 255), retangulo_novo_jogo)
    tela.blit(texto_novo_jogo, (235, 260))

    texto_sair = font_botao.render("Sair", True, (255, 0, 0))
    retangulo_sair = pygame.Rect(225, 320, 150, 50)
    pygame.draw.rect(tela, (255, 255, 255), retangulo_sair)
    tela.blit(texto_sair, (270, 330))

    pygame.display.update()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if retangulo_novo_jogo.collidepoint(evento.pos):
                    return True  # Novo jogo
                elif retangulo_sair.collidepoint(evento.pos):
                    rodando = False  # Fechar o jogo

    return False  # Caso o jogador saia

def main():
    pygame.init()

    largura, altura = 600, 400
    tamanho = 20
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Jogo da Cobrinha - POO")
    relogio = pygame.time.Clock()

    recorde = carregar_recorde()  # Carregar o recorde

    cobra = Cobra(largura // 2, altura // 2, tamanho)
    comida = Comida(random.randint(0, (largura - tamanho) // tamanho) * tamanho,
                    random.randint(0, (altura - tamanho) // tamanho) * tamanho,
                    tamanho)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    cobra.mudar_direcao("CIMA")
                elif evento.key == pygame.K_DOWN:
                    cobra.mudar_direcao("BAIXO")
                elif evento.key == pygame.K_LEFT:
                    cobra.mudar_direcao("ESQUERDA")
                elif evento.key == pygame.K_RIGHT:
                    cobra.mudar_direcao("DIREITA")

        cobra.mover()

        if cobra._corpo[0][0] == comida._x and cobra._corpo[0][1] == comida._y:
            cobra.comer()
            comida.reposicionar(largura, altura)

        if cobra.colidiu(largura, altura):
            # Verifica se o jogador atingiu um novo recorde
            if cobra.pontos > recorde:
                recorde = cobra.pontos
                salvar_recorde(recorde)  # Atualiza o arquivo com o novo recorde

            if mostrar_tela_fim_de_jogo(tela, cobra.pontos, recorde):
                # Novo jogo
                cobra = Cobra(largura // 2, altura // 2, tamanho)
                comida = Comida(random.randint(0, (largura - tamanho) // tamanho) * tamanho,
                                random.randint(0, (altura - tamanho) // tamanho) * tamanho,
                                tamanho)
            else:
                rodando = False  # Fechar o jogo após sair

        tela.fill((0, 0, 0))
        cobra.desenhar(tela)
        comida.desenhar(tela)
        pygame.display.update()
        relogio.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()