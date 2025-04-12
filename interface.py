import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dao.pessoa_dao import PessoaDAO
from classes.pessoa import Pessoa
from dao.estoque_dao import EstoqueDAO
from dao.pedido_dao import PedidoDAO

class AppLoja:
    def __init__(self, master):
        self.master = master
        self.master.title("Loja Virtual - Distribuidora Bebidas S.A")
        self.master.geometry("500x250")
        
        self.create_widgets()
    
    def create_widgets(self):
        title = tk.Label(self.master, text="Bem-vindo à Loja Virtual", font=("Arial", 30))
        title.pack()

        separator = tk.Frame(self.master, height=2, bd=0, bg="gray")
        separator.pack(fill='x', padx=20, pady=10)

        frame = tk.Frame(self.master)
        frame.pack()

        login_label = tk.Label(frame, text="Login de Usuário", font=("Arial", 16))
        login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=10)

        user_label = tk.Label(frame, text="E-mail", font=("Arial", 12))
        user_label.grid(row=1, column=0)

        self.user_entry = tk.Entry(frame, width=20)
        self.user_entry.grid(row=1, column=1, pady=10)

        password_label = tk.Label(frame, text="Senha", font=("Arial", 12))
        password_label.grid(row=2, column=0)

        self.password_entry = tk.Entry(frame, show='*', width=20)
        self.password_entry.grid(row=2, column=1)

        login_button = tk.Button(frame, text='Entrar', font=('Arial', 10), command=self.login)
        login_button.grid(row=3, column=0, pady=10)

        sign_up_button = tk.Button(frame, text='Registrar', font=('Arial', 10), command=self.registrar)
        sign_up_button.grid(row=3, column=1)

    def login(self):
        email = self.user_entry.get()
        senha = self.password_entry.get()

        pessoa = PessoaDAO.verifica_email_senha(email, senha)

        if pessoa:
            if pessoa.tipo == "admin":
                messagebox.showinfo("Login", f"Bem-vindo administrador {pessoa.nome}!")
            elif pessoa.tipo == "funcionario":
                messagebox.showinfo("Login", f"Bem-vindo funcionário {pessoa.nome}!")
            else:
                messagebox.showinfo("Login", f"Bem-vindo, {pessoa.nome}!")
                JanelaCliente(self.master, cliente=pessoa)
        else:
            messagebox.showerror("Erro de Login", "E-mail ou senha incorretos, ou usuário não registrado.") 

    def registrar(self):
        janela_registro = tk.Toplevel(self.master)
        janela_registro.title("Registro de cliente")
        janela_registro.geometry("400x300")

        labels =  ["Nome", "CPF/CNPJ", "Endereço", "Telefone", "E-mail", "Senha"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(janela_registro, text=label).grid(row=i, column=0, sticky="e", pady=5)
            entry = tk.Entry(janela_registro, width=30, show='*' if label == "Senha" else '')
            entry.grid(row=i, column=1, pady=5)
            entries[label] = entry

        def confirma_registro():
            pessoa = Pessoa(
                nome=entries["Nome"].get(),
                cpf_cnpj=entries["CPF/CNPJ"].get(),
                endereco=entries["Endereço"].get(),
                telefone=entries["Telefone"].get(),
                email=entries["E-mail"].get(),
                senha=entries["Senha"].get(),
                tipo="cliente"
        )
            
            try:
                PessoaDAO.criar(pessoa)
                messagebox.showinfo("Sucesso", "Cliente registrado com sucesso!")
                janela_registro.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao registrar: {str(e)}")

        btn = tk.Button(janela_registro, text="Confirmar Registro", command=confirma_registro)
        btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

class JanelaCliente(tk.Toplevel):
    def __init__(self, master=None, cliente=None):
        super().__init__(master)
        self.title("Produtos Disponíveis")
        self.geometry("800x600")
        self.cliente = cliente

        self.carrinho = []
        self.valor_total = 0.0

        self.categorias = ["Todos", "Refrigerante", "Cerveja", "Agua Mineral", "Sucos"]
        self.combo_categoria = ttk.Combobox(self, values=self.categorias, state="readonly")
        self.combo_categoria.set("Todos")
        self.combo_categoria.pack(pady=10)
        self.combo_categoria.bind("<<ComboboxSelected>>", self.filtrar_categoria)

        # Tabela de produtos
        self.tree = ttk.Treeview(self, columns=("Nome", "Preço", "Quantidade"), show='headings')
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Preço", text="Preço")
        self.tree.heading("Quantidade", text="Qtd Estoque")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.carregar_todos()

        frame_compra = tk.Frame(self)
        frame_compra.pack(pady=10)

        tk.Label(frame_compra, text="Quantidade: ").grid(row=0, column=0)
        self.entry_qtd = tk.Entry(frame_compra, width=5)
        self.entry_qtd.grid(row=0, column=1)

        tk.Button(frame_compra, text="Adicionar ao carrinho", command=self.adicionar_ao_carrinho).grid(row=0, column=2, padx=5)

        self.lista_carrinho = tk.Listbox(self, width=100)
        self.lista_carrinho.pack(padx=10, pady=5)

        self.label_total = tk.Label(self, text="Total: R$ 0.00", font=("Arial", 14))
        self.label_total.pack(pady=5)

        tk.Label(self, text="Seu time:").pack()
        self.entry_time = tk.Entry(self)
        self.entry_time.pack()

        tk.Label(self, text="Forma de Pagamento:").pack()
        self.combo_pagamento = ttk.Combobox(self, values=["pix", "boleto", "cartao"], state="readonly")
        self.combo_pagamento.pack()

        tk.Button(self, text="Finalizar Compra", command=self.finalizar_compra).pack(pady=10)

    def carregar_todos(self):
        self.tree.delete(*self.tree.get_children())
        produtos = EstoqueDAO.lista_tudo()
        for produto in produtos:
            self.tree.insert("", tk.END, values=(produto.nome, float(produto.preco), produto.quantidade))

    def filtrar_categoria(self, event):
        categoria = self.combo_categoria.get()
        self.tree.delete(*self.tree.get_children())

        if categoria == "Todos":
            produtos = EstoqueDAO.lista_tudo()
        else:
            produtos = EstoqueDAO.procura_categoria(categoria)

        for produto in produtos:
            self.tree.insert("", tk.END, values=(produto.nome, float(produto.preco), produto.quantidade))

    def adicionar_ao_carrinho(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Selecione um produto", "Escolha um produto.")
            return
        
        try:
            qtd = int(self.entry_qtd.get())
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Informe uma quantidade válida!")
            return
        
        nome, preco, estoque = self.tree.item(item)["values"]
        if qtd > int(estoque):
            messagebox.showerror("Erro", "Quantidade maior que o estoque.")
            return
        
        produto = EstoqueDAO.procura_nome(nome)
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return
        
        subtotal = float(produto.preco) * qtd
        self.carrinho.append((produto, qtd, float(produto.preco)))
        self.lista_carrinho.insert(tk.END, f"{produto.nome} - {qtd} un - R$ {subtotal:.2f}")
        self.valor_total +=subtotal
        self.label_total.config(text=f"Total: R$ {self.valor_total:.2f}")

    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showwarning("Carrinho vazio", "Adicione produtos ao carrinho.")
            return
            
        time = self.entry_time.get().lower()
        forma_pagamento = self.combo_pagamento.get()

        if not forma_pagamento:
            messagebox.showerror("Erro", "Escolha uma forma de pagamento.")
            return
            
        if time == "Flamengo":
            self.valor_total *= 1.05
        elif time == "Fluminense":
            self.valor_total *= 0.90

        id_pagamento = PedidoDAO.get_id_pagamento(forma_pagamento)

        id_venda = PedidoDAO.criar_venda(self.cliente.id, id_pagamento, self.valor_total)

        for produto, qtd, preco in self.carrinho:
            PedidoDAO.adicionar_detalhe_venda(id_venda, produto.id, qtd, preco)
            EstoqueDAO.atualizar_quantidade(produto.id, produto.quantidade - qtd)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppLoja(root)
    root.mainloop()