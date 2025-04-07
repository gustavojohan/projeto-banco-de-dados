from database.database import Database
from classes.pessoa import Pessoa

class PessoaDAO:
    # INSERIR
    @staticmethod
    def criar(pessoa):
        conn = Database.conectar()
        cursor = conn.cursor()

        sql = "INSERT INTO pessoas (nome, cpf_cnpj, endereco, telefone, email) VALUES (%s, %s, %s, %s, %s)"
        valores = (pessoa.nome, pessoa.cpf_cnpj, pessoa.endereco, pessoa.telefone, pessoa.email)

        cursor.execute(sql, valores)
        conn.commit()

        # Obtem o id retornado pelo MySQL
        pessoa.id = cursor.lastrowid

        cursor.close()
        conn.close()

    # ALTERAR
    @staticmethod
    def atualiza(pessoa):
        conn = Database.conectar()
        cursor = conn.cursor()

        campos_disponiveis = ["nome", "cpf_cnpj", "endereco", "telefone", "email"]
        
        campos_para_atualizar = []
        valores = []

        for campo in campos_disponiveis:
            valor = getattr(pessoa, campo, None)
            if valor is not None:
                campos_para_atualizar.append(f"{campo} = %s")
                valores.append(valor)

        if not campos_para_atualizar:
            conn.close()
            raise ValueError("Nenhum campo foi inserido para atualização.")
        
        valores.append(pessoa.id)

        sql = f"UPDATE pessoas SET {', '.join(campos_para_atualizar)} WHERE id = %s"
        cursor.execute(sql, valores)
        conn.commit()

        cursor.close()
        conn.close()
        
    # PESQUISAR POR NOME
    @staticmethod
    def procura_nome(nome):
        conn = Database.conectar()
        cursor = conn.cursor()

        sql = "SELECT * FROM pessoas WHERE nome = %s"
        cursor.execute(sql, (nome,))

        registros = cursor.fetchall() # retorna todas as linhas do resultado

        pessoa = [Pessoa(id=linha[0], nome=linha[1], cpf_cnpj=linha[2], endereco=linha[3], telefone=linha[4], email=linha[5]) for linha in registros]

        cursor.close()
        conn.close()

        return pessoa

    # REMOVER
    @staticmethod
    def remover_id(id):
        conn  = Database.conectar()
        cursor = conn.cursor()

        sql = "DELETE FROM pessoas WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

        cursor.close()
        conn.close()
    
    # LISTAR TODOS
    @staticmethod
    def lista_tudo():
        conn  = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM pessoas")
        registros = cursor.fetchall() # retorna todas as linhas do resultado

        array_pessoas = [Pessoa(id=linha[0], nome=linha[1], cpf_cnpj=linha[2], endereco=linha[3], telefone=linha[4], email=linha[5]) for linha in registros]

        cursor.close()
        conn.close()

        return array_pessoas
    
    # EXIBIR UM
    @staticmethod
    def lista_uma(id):
        conn  = Database.conectar()
        cursor = conn.cursor()

        sql = "SELECT * FROM pessoas WHERE id = %s"
        cursor.execute(sql, (id,))
        registros = cursor.fetchone() # retorna uma linha

        if registros:
            pessoa = [Pessoa(id=registros[0], nome=registros[1], cpf_cnpj=registros[2], endereco=registros[3], telefone=registros[4], email=registros[5])]
        else:
            pessoa = None

        cursor.close()
        conn.close()

        return pessoa
    
    
    
