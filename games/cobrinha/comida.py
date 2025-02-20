import pygame
import random
import requests
from io import BytesIO
from entidade import Entidade

class Comida(Entidade):
    def __init__(self, x, y, tamanho):
        super().__init__(x, y, tamanho)
        
        # Baixar a imagem do link e carregá-la no Pygame
        url = "https://www.imagenspng.com.br/wp-content/uploads/2015/04/branca-de-neve-cute-maca-06.png"
        response = requests.get(url)
        imagem_raw = BytesIO(response.content)
        self.imagem = pygame.image.load(imagem_raw)
        
        # Redimensionar a imagem para o tamanho especificado
        self.imagem = pygame.transform.scale(self.imagem, (tamanho, tamanho))

    def desenhar(self, tela):
        # Desenhar a imagem da comida
        tela.blit(self.imagem, (self._x, self._y))

    def reposicionar(self, largura, altura):
        self._x = random.randint(0, (largura - self._tamanho) // self._tamanho) * self._tamanho
        self._y = random.randint(0, (altura - self._tamanho) // self._tamanho) * self._tamanho