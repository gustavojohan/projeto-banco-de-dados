import tkinter as tk
from classes.estoque import Estoque
from dao.estoque_dao import EstoqueDAO
from classes.pessoa import Pessoa
from dao.pessoa_dao import PessoaDAO
from tabulate import tabulate

def lista_pessoa(metodo):
    dados = [(p.id, p.nome, p.cpf_cnpj, p.endereco, p.telefone, p.email) for p in metodo]
    cabecalho = ["ID", "Nome", "CPF/CNPJ", "Endereço", "Telefone", "Email"]

    print(tabulate(dados, headers=cabecalho, tablefmt="grid"))

def lista_estoque(metodo):
    dados = [(e.id, e.nome, e.preco, e.quantidade, e.categoria) for e in metodo]
    cabecalho = ["ID", "Nome", "Preco", "Quantidade", "Categoria"]

    print(tabulate(dados, headers=cabecalho, tablefmt="grid"))

# Janela
root = tk.Tk()
root.title("Loja Virtual - Distribuidora Bebidas S.A")
root.geometry("500x250")

frame = tk.Frame()


# Titulo loja
title = tk.Label(root, text = "Bem-vindo à Loja Virtual", font=("Arial", 30))
title.pack()


separator = tk.Frame(root, height=2, bd=0, bg="gray")
separator.pack(fill='x', padx=20, pady=10)

login_label = tk.Label(frame, text="Login de Usuário", font=("Arial", 16))
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=10)

user_label = tk.Label(frame, text="E-mail", font=("Arial", 12))
user_label.grid(row=1, column=0)

user_entry_label = tk.Entry(frame, width=20)
user_entry_label.grid(row=1, column=1, pady=10)

password_label = tk.Label(frame, text="Senha", font=("Arian", 12))
password_label.grid(row=2, column=0)

password_entry_label = tk.Entry(frame, show='*', width=20)
password_entry_label.grid(row=2, column=1)

login_button = tk.Button(frame, text='Entrar', font=('Arial', 10))
login_button.grid(row=3, column=0, pady=10)

sign_up_button = tk.Button(frame, text='Registrar', font=('Arial', 10))
sign_up_button.grid(row=3, column=1, columnspan=2)

frame.pack()


root.mainloop()


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