class Pessoa:
    def __init__(self, id=None, nome="", cpf_cnpj="", endereco="", telefone="", email=""):
        self.id = id
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.endereco = endereco
        self.telefone = telefone
        self.email = email

    def __str__(self):
        return f"Pessoa(id={self.id}, nome={self.nome}, cpf_cnpj={self.cpf_cnpj}, endereco={self.endereco}, telefone={self.telefone}, email={self.email})"