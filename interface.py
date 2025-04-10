import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dao.pessoa_dao import PessoaDAO
from classes.pessoa import Pessoa
from dao.estoque_dao import EstoqueDAO

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
                JanelaCliente(self.master)
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
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Produtos Disponíveis")
        self.geometry("600x400")

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

    def carregar_todos(self):
        self.tree.delete(*self.tree.get_children())
        produtos = EstoqueDAO.lista_tudo()
        for produto in produtos:
            self.tree.insert("", tk.END, values=(produto.nome, produto.preco, produto.quantidade))

    def filtrar_categoria(self, event):
        categoria = self.combo_categoria.get()
        self.tree.delete(*self.tree.get_children())

        if categoria == "Todos":
            produtos = EstoqueDAO.lista_tudo()
        else:
            produtos = EstoqueDAO.procura_categoria(categoria)

        for produto in produtos:
            self.tree.insert("", tk.END, values=(produto.nome, produto.preco, produto.quantidade))

if __name__ == "__main__":
    root = tk.Tk()
    app = AppLoja(root)
    root.mainloop()