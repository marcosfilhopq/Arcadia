import pygame
from entidade import Entidade

class Cobra(Entidade):
    def __init__(self, x, y, tamanho):
        super().__init__(x, y, tamanho)
        self._corpo = [[x, y]]
        self._direcao = "DIREITA"
        self._crescer = False
        self.pontos = 0

    def mover(self):
        if self._direcao == "CIMA":
            nova_cabeca = [self._corpo[0][0], self._corpo[0][1] - self._tamanho]
        elif self._direcao == "BAIXO":
            nova_cabeca = [self._corpo[0][0], self._corpo[0][1] + self._tamanho]
        elif self._direcao == "ESQUERDA":
            nova_cabeca = [self._corpo[0][0] - self._tamanho, self._corpo[0][1]]
        elif self._direcao == "DIREITA":
            nova_cabeca = [self._corpo[0][0] + self._tamanho, self._corpo[0][1]]

        self._corpo.insert(0, nova_cabeca)
        if not self._crescer:
            self._corpo.pop()
        self._crescer = False

    def mudar_direcao(self, direcao):
        if direcao == "CIMA" and self._direcao != "BAIXO":
            self._direcao = direcao
        elif direcao == "BAIXO" and self._direcao != "CIMA":
            self._direcao = direcao
        elif direcao == "ESQUERDA" and self._direcao != "DIREITA":
            self._direcao = direcao
        elif direcao == "DIREITA" and self._direcao != "ESQUERDA":
            self._direcao = direcao

    def comer(self):
        self._crescer = True
        self.pontos += 1

    def desenhar(self, tela):
        # Desenhar o fundo verde escuro com detalhes de grama
        tela.fill((34, 139, 34))  # Cor de fundo verde escuro
        for i in range(0, tela.get_width(), 20):
            for j in range(0, tela.get_height(), 20):
                pygame.draw.line(tela, (85, 107, 47), (i, j), (i + 10, j + 10), 1)
                pygame.draw.line(tela, (85, 107, 47), (i + 10, j), (i, j + 10), 1)

        # Desenhar os segmentos da cobra
        for segmento in self._corpo:
            pygame.draw.circle(tela, (0, 0, 139), (segmento[0] + self._tamanho // 2, segmento[1] + self._tamanho // 2), self._tamanho // 2)

        # Desenhar os olhos da cobra
        if len(self._corpo) > 0:
            olho_tamanho = 4  # Tamanho dos olhos
            # Olho esquerdo
            pygame.draw.circle(tela, (255, 255, 255), (self._corpo[0][0] + self._tamanho // 3, self._corpo[0][1] + self._tamanho // 3), olho_tamanho)
            # Olho direito
            pygame.draw.circle(tela, (255, 255, 255), (self._corpo[0][0] + 2 * self._tamanho // 3, self._corpo[0][1] + self._tamanho // 3), olho_tamanho)

        # Desenhar o contador de pontos na parte superior
        font = pygame.font.SysFont(None, 36)
        texto = font.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        tela.blit(texto, (10, 10))  # Desenha o contador no canto superior esquerdo

    def colidiu(self, largura, altura):
        if (
            self._corpo[0][0] < 0 or self._corpo[0][0] >= largura or
            self._corpo[0][1] < 0 or self._corpo[0][1] >= altura
        ):
            return True
        if self._corpo[0] in self._corpo[1:]:
            return True
        return False