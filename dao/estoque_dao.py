from database.database import Database
from classes.estoque import Estoque

class EstoqueDAO:
    # INSERIR
    @staticmethod
    def criar(produto):
        conn = Database.conectar()
        cursor = conn.cursor()

        sql = "INSERT INTO estoque (nome, preco, quantidade, categoria) VALUES (%s, %s, %s, %s)"
        valores = (produto.nome, produto.preco, produto.quantidade, produto.categoria)

        cursor.execute(sql, valores)
        conn.commit()

        # Obtem o id retornado pelo MySQL
        produto.id = cursor.lastrowid

        cursor.close()
        conn.close()

    # ALTERAR
    @staticmethod
    def atualiza(produto):
        conn = Database.conectar()
        cursor = conn.cursor()

        campos_disponiveis = ["nome", "preco", "quantidade", "categoria"]

        campos_para_atualizar = []
        valores = []

        for campo in campos_disponiveis:
            valor = getattr(produto, campo, None)
            if valor is not None:
                campos_para_atualizar.append(f"{campo} = %s")
                valores.append(valor)
        
        if not campos_para_atualizar:
            conn.close()
            raise ValueError("Nenhum campo foi inserido para atualização.")
        
        valores.append(produto.id)

        sql = f"UPDATE estoque SET {', '.join(campos_para_atualizar)} WHERE id = %s"
        cursor.execute(sql, valores)
        conn.commit()

        cursor.close()
        conn.close

    @staticmethod
    def atualizar_quantidade(id_produto, nova_quantidade):
        conn = Database.conectar()
        cursor = conn.cursor()

        sql = "UPDATE estoque SET quantidade = %s WHERE id = %s"
        cursor.execute(sql, (nova_quantidade, id_produto))

        conn.commit()
        cursor.close()
        conn.close()

    # PESQUISAR POR CATEGORIA
    @staticmethod
    def procura_categoria(categoria):
        conn = Database.conectar()
        cursor = conn.cursor()

        sql = "SELECT * FROM vw_produtos_disponiveis WHERE categoria = %s"
        cursor.execute(sql, (categoria,))

        registros = cursor.fetchall()

        produto = [Estoque(id=linha[0], nome=linha[1], preco=linha[2], quantidade=linha[3], categoria=linha[4]) for linha in registros]

        cursor.close()
        conn.close()

        return produto
    
    @staticmethod
    def procura_nome(nome):
        conn = Database.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estoque WHERE nome = %s", (nome,))
        registro = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if registro:
            return Estoque(id=registro[0], nome=registro[1], preco=registro[2], 
                        quantidade=registro[3], categoria=registro[4])
        return None
    """def procura_nome(nome):
        conn = Database.conectar()
        cursor = conn.cursor()

        sql = "SELECT * FROM estoque WHERE nome = %s"
        cursor.execute(sql, (nome,))

        registros = cursor.fetchall() # retorna todas as linhas do resultado

        estoque = [Estoque(id=linha[0], nome=linha[1], preco=linha[2], quantidade=linha[3], categoria=linha[4]) for linha in registros]

        cursor.close()
        conn.close()

        return estoque"""
    
    # REMOVER
    @staticmethod
    def remover_id(id):
        conn  = Database.conectar()
        cursor = conn.cursor()

        sql = "DELETE FROM estoque WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

        cursor.close()
        conn.close()

    # LISTAR TODOS
    @staticmethod
    def lista_tudo():
        conn  = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM estoque")
        registros = cursor.fetchall() # retorna todas as linhas do resultado

        array_estoque = [Estoque(id=linha[0], nome=linha[1], preco=linha[2], quantidade=linha[3], categoria=linha[4]) for linha in registros]

        cursor.close()
        conn.close()

        return array_estoque
    
    # EXIBIR UM 
    @staticmethod
    def lista_um(id):
        conn  = Database.conectar()
        cursor = conn.cursor()

        sql = "SELECT * FROM estoque WHERE id = %s"
        cursor.execute(sql, (id,))
        registro = cursor.fetchone() # retorna uma linha

        if registro:
            produto = [Estoque(id=registro[0], nome=registro[1], preco=registro[2], quantidade=registro[3], categoria=registro[4])]
        else:
            produto = None

        cursor.close()
        conn.close()

        return produto