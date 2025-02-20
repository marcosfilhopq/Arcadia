class Entidade:
    def __init__(self, x, y, tamanho):
        self._x = x  # Encapsulamento (atributo protegido)
        self._y = y
        self._tamanho = tamanho

    def desenhar(self, tela):
        raise NotImplementedError("Método desenhar deve ser implementado pelas subclasses.")  # Polimorfismo