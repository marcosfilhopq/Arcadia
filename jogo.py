class JogoForca:
    def __init__(self, palavra):
        self.palavra = palavra.lower()
        self.acertos = ["_" for _ in palavra]
        self.tentativas = 6

    def tentar_letra(self, letra):
        if letra in self.palavra:
            for i, l in enumerate(self.palavra):
                if l == letra:
                    self.acertos[i] = letra
        else:
            self.tentativas -= 1
        return "".join(self.acertos), self.tentativas
