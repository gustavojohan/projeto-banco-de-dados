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
                JanelaMenuFuncionario(self.master, funcionario=pessoa)
            else:
                messagebox.showinfo("Login", f"Bem-vindo, {pessoa.nome}!")
                JanelaMenuCliente(self.master, cliente=pessoa)
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

class JanelaMenuCliente(tk.Toplevel):
    def __init__(self, master=None, cliente=None):
        super().__init__(master)
        self.title("Menu do Cliente")
        self.geometry("400x300")
        self.cliente = cliente

        tk.Label(self, text=f"Olá, {cliente.nome}!", font=("Arial", 16)).pack(pady=20)

        botao_comprar = tk.Button(self, text="Fazer Compras", width=25, command=self.ir_para_compras)
        botao_comprar.pack(pady=10)

        botao_historico = tk.Button(self, text="Histórico de Compras", width=25, command=self.mostrar_historico)
        botao_historico.pack(pady=10)

        botao_dados = tk.Button(self, text="Exibir Dados Pessoais", width=25, command=self.exibir_dados)
        botao_dados.pack(pady=10)

    def ir_para_compras(self):
        self.destroy()
        JanelaCliente(self.master, cliente=self.cliente)

    def mostrar_historico(self):
        historico = PedidoDAO.historico_compras(self.cliente.id)
        if not historico:
            messagebox.showinfo("Histórico", "Nenhuma compra encontrada.")
            return
        historico_str = "\n\n".join(
            f"ID: {h[0]}, Valor: R$ {h[1]:.2f}, Status: {h[2]}, Data: {h[3]}"
            for h in historico
        )
        messagebox.showinfo("Histórico de Compras", historico_str)

    def exibir_dados(self):
        dados = (
            f"Nome: {self.cliente.nome}\n"
            f"CPF/CNPJ: {self.cliente.cpf_cnpj}\n"
            f"Endereço: {self.cliente.endereco}\n"
            f"Telefone: {self.cliente.telefone}\n"
            f"E-mail: {self.cliente.email}"
        )
        messagebox.showinfo("Seus Dados", dados)

class JanelaCliente(tk.Toplevel):
    def __init__(self, master=None, cliente=None):
        super().__init__(master)
        self.title("Produtos Disponíveis")
        self.geometry("900x800")
        self.cliente = cliente

        self.carrinho = []
        self.valor_total = 0.0

        self.categorias = ["Todos", "Refrigerante", "Cerveja", "Agua Mineral", "Sucos"]
        self.combo_categoria = ttk.Combobox(self, values=self.categorias, state="readonly")
        self.combo_categoria.set("Todos")
        self.combo_categoria.pack(pady=10)
        self.combo_categoria.bind("<<ComboboxSelected>>", self.filtrar_categoria)

        # Filtros
        frame_filtros = tk.Frame(self)
        frame_filtros.pack(pady=5)

        tk.Label(frame_filtros, text="Nome:").grid(row=0, column=0)
        self.entry_nome = tk.Entry(frame_filtros, width=20)
        self.entry_nome.grid(row=0, column=1, padx=5)

        tk.Label(frame_filtros, text="Preço Mín:").grid(row=0, column=2)
        self.entry_preco_min = tk.Entry(frame_filtros, width=7)
        self.entry_preco_min.grid(row=0, column=3, padx=5)

        tk.Label(frame_filtros, text="Preço Máx:").grid(row=0, column=4)
        self.entry_preco_max = tk.Entry(frame_filtros, width=7)
        self.entry_preco_max.grid(row=0, column=5, padx=5)

        tk.Button(frame_filtros, text="Aplicar Filtros", command=self.aplicar_filtros).grid(row=0, column=6, padx=5)

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
        
        desconto_porcentagem = 0.0
        valor_original = self.valor_total
            
        if time == "flamengo":
            desconto_porcentagem = -0.05
            valor_final = valor_original * 1.05
            messagebox.showinfo(
                "Atenção",
                f"Por torcer para o Flamengo, houve um acréscimo de 5% no valor total da sua compra."
                f"Valor original: R$ {valor_original:.2f}\n"
                f"Valor com acréscimo: R$ {valor_final:.2f}"
            )
        elif time == "fluminense":
            desconto_porcentagem = 0.10
            valor_final = valor_original * 0.90
            messagebox.showinfo(
                "Desconto Aplicado",
                f"Parabéns! Por torcer para o Fluminense, você recebeu um desconto de 10% na sua compra."
                f"Valor original: R$ {valor_original:.2f}\n"
                f"Valor com desconto: R$ {valor_final:.2f}"
            )
        else:
            valor_final = valor_original

        self.valor_total = valor_final

        id_pagamento = PedidoDAO.get_id_pagamento(forma_pagamento)
        id_venda = PedidoDAO.criar_venda(self.cliente.id, id_pagamento, self.valor_total)

        for produto, qtd, preco in self.carrinho:
            desconto_unitario = preco * desconto_porcentagem
            preco_unitario_com_desconto = preco - desconto_unitario
            PedidoDAO.adicionar_detalhe_venda(id_venda, produto.id, qtd, preco_unitario_com_desconto, desconto_unitario)
            EstoqueDAO.atualizar_quantidade(produto.id, produto.quantidade - qtd)

        messagebox.showinfo(
            "Compra Realizada",
            "Sua compra foi registrada com sucesso!\nEla está em análise e aguarda a aprovação."
        )

        # Limpa o carrinho ao finalizar a compra
        self.carrinho.clear()
        self.lista_carrinho.delete(0, tk.END)
        self.valor_total = 0.0
        self.label_total.config(text="Total: R$ 0.00")
        self.entry_time.delete(0, tk.END)
        self.combo_pagamento.set('')

    def aplicar_filtros(self):
        nome = self.entry_nome.get().strip()
        try:
            preco_min = float(self.entry_preco_min.get()) if self.entry_preco_min.get() else None
            preco_max = float(self.entry_preco_max.get()) if self.entry_preco_max.get() else None
        except ValueError:
            messagebox.showerror("Erro", "Informe valores numéricos válidos para os preços.")
            return

        produtos = EstoqueDAO.filtrar(nome, preco_min, preco_max, self.combo_categoria.get())
        
        self.tree.delete(*self.tree.get_children())
        for produto in produtos:
            self.tree.insert("", tk.END, values=(produto.nome, float(produto.preco), produto.quantidade))

class JanelaMenuFuncionario(tk.Toplevel):
    def __init__(self, master=None, funcionario=None):
        super().__init__(master)
        self.title("Menu do Funcionário")
        self.geometry("400x300")
        self.funcionario = funcionario

        tk.Label(self, text=f"Olá, {funcionario.nome}!", font=("Arial", 16)).pack(pady=20)

        botao_analise_pedidos = tk.Button(self, text="Análise de Pedidos", width=25, command=self.ir_para_analise)
        botao_analise_pedidos.pack(pady=10)

        botao_baixo_estoque = tk.Button(self, text="Verificar Estoque", width=25, command=self.mostra_estoque)
        botao_baixo_estoque.pack(pady=10)

        """botao_adicionar_produtos = tk.Button(self, text="Adicionar Produtos ao Estoque", width=25, command=self.adiciona_estoque)
        botao_adicionar_produtos.pack(pady=10)"""

    def ir_para_analise(self):
        #self.destroy()
        JanelaAnalisePedidos(self)

    def mostra_estoque(self):
        estoque_baixo = EstoqueDAO.listar_estoque_baixo()

        janela = tk.Toplevel(self)
        janela.title("Produtos com Estoque Baixo")
        janela.geometry("700x300")

        tree = ttk.Treeview(janela, columns=("Nome", "Preço", "Quantidade"), show='headings')
        tree.heading("Nome", text="Nome")
        tree.heading("Preço", text="Preço")
        tree.heading("Quantidade", text="Quantidade em Estoque")

        tree.pack(expand=True, fill="both", padx=10, pady=10)

        for nome, preco, quantidade in estoque_baixo:
            tree.insert("", tk.END, values=(nome, float(preco), quantidade))

        if not estoque_baixo:
            tk.Label(janela, text="Nenhum produto em baixo estoque.").pack(pady=10)


class JanelaAnalisePedidos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Análise de Pedidos")
        self.geometry("700x400")

        self.tree = ttk.Treeview(self, columns=("ID", "Cliente", "Total", "Data"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Data", text="Data")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        frame_btns = tk.Frame(self)
        frame_btns.pack(pady=10)

        tk.Button(frame_btns, text="Concluir Pedido", command=self.concluir).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_btns, text="Reprovar Pedido", command=self.reprovar).pack(side=tk.LEFT, padx=10)

        self.carregar_pedidos()

    def carregar_pedidos(self):
        self.tree.delete(*self.tree.get_children())
        pedidos = PedidoDAO.listar_pedidos_em_analise()
        for pedido in pedidos:
            self.tree.insert("", tk.END, values=(pedido['id'], pedido['cliente'], pedido['valor_total'], pedido['data_solicitacao']))

    def concluir(self):
        self._atualizar_status('concluido')

    def reprovar(self):
        self._atualizar_status('cancelado')

    def _atualizar_status(self, status):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um pedido.")
            return

        id_venda = self.tree.item(item)["values"][0]
        PedidoDAO.atualizar_status_pedido(id_venda, status)
        messagebox.showinfo("Sucesso", f"Pedido {status} com sucesso!")
        self.carregar_pedidos()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppLoja(root)
    root.mainloop()