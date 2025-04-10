from classes.estoque import Estoque
from dao.estoque_dao import EstoqueDAO
from classes.pessoa import Pessoa
from dao.pessoa_dao import PessoaDAO
from interface import AppLoja
from interface import JanelaCliente
import tkinter as tk
from tabulate import tabulate


def lista_pessoa(metodo):
    dados = [(p.id, p.nome, p.cpf_cnpj, p.endereco, p.telefone, p.email) for p in metodo]
    cabecalho = ["ID", "Nome", "CPF/CNPJ", "Endereço", "Telefone", "Email"]

    print(tabulate(dados, headers=cabecalho, tablefmt="grid"))

def lista_estoque(metodo):
    dados = [(e.id, e.nome, e.preco, e.quantidade, e.categoria) for e in metodo]
    cabecalho = ["ID", "Nome", "Preco", "Quantidade", "Categoria"]

    print(tabulate(dados, headers=cabecalho, tablefmt="grid"))


def main():
    root = tk.Tk()
    app = AppLoja(root)
    root.mainloop()

if __name__ == "__main__":
    main()


'''lista_pessoa(PessoaDAO.lista_tudo())

x = input()

# INSERE
pessoa = Pessoa(nome="Zacarias", cpf_cnpj="98155564312", endereco="Rua T", telefone="85943256666", email="zaca999@gmail.com")
PessoaDAO.criar(pessoa)

# ALTERA
pessoa = Pessoa(id=1, nome = None, cpf_cnpj=None, endereco=None, telefone="83988877666", email="allana_lara@gmail.com")
PessoaDAO.atualiza(pessoa)

# REMOVER POR ID 8
PessoaDAO.remover_id('8')

x = input()

# PESQUISA POR NOME
print('Clientes encontrados:')
lista_pessoa(PessoaDAO.procura_nome('José da Silva'))

# LISTA TODOS
print('\nClientes cadastrados:')
lista_pessoa(PessoaDAO.lista_tudo())

# EXIBE UM
print('\n\nListando a pessoa de id 14:')
lista_pessoa(PessoaDAO.lista_uma(14))

x = input()

'''

# ESTOQUE

'''

lista_estoque(EstoqueDAO.lista_tudo())

# INSERE
produto = Estoque(nome='Suco de Laranja OQ 1l', preco='14.90', quantidade='50', categoria='Sucos')
EstoqueDAO.criar(produto)

# ALTERA
produto = Estoque(id=3, nome=None, preco=None, quantidade='250', categoria=None)
EstoqueDAO.atualiza(produto)
produto = Estoque(id=7, nome=None, preco='35.90', quantidade=None, categoria=None)
EstoqueDAO.atualiza(produto)


x = input()

lista_estoque(EstoqueDAO.lista_tudo())

# REMOVER POR ID
EstoqueDAO.remover_id('7')

x = input()

# PESQUISA POR CATEGORIA
print('Produtos encontrados:')
lista_estoque(EstoqueDAO.procura_categoria('Refrigerante'))

# LISTA TUDO
print('\nProdutos cadastrados:')
lista_estoque(EstoqueDAO.lista_tudo())

#EXIBE UM
print('\n\nListando o produto de id 9:')
lista_estoque(EstoqueDAO.lista_um(9))
'''''''''