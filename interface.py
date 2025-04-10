import tkinter as tk

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
        print(f"Login com: {email} - {senha}")

    def registrar(self):
        print("Abrir tela de registro...")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppLoja(root)
    root.mainloop()