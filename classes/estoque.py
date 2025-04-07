class Estoque:
    def __init__(self, id=None, nome="", preco="", quantidade="", categoria=""):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.categoria = categoria


    def __str__(self):
        return f"Estoque(id={self.id}, nome={self.nome}, preco={self.preco}, quantidade={self.quantidade}, categoria={self.categoria})"