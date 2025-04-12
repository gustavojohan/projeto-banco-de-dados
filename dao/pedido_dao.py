from database.database import Database

class PedidoDAO:
    @staticmethod
    def get_id_pagamento(nome_pagamento):
        conn = Database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM formas_pagamento WHERE nome = %s", (nome_pagamento,))
        id_pagamento = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return id_pagamento
    
    @staticmethod
    def criar_venda(id_cliente, id_pagamento, valor_total):
        conn = Database.conectar()
        cursor = conn.cursor()

        sql = "INSERT INTO vendas (id_cliente, id_pagamento, valor_total) VALUES (%s, %s, %s)"
        cursor.execute(sql, (id_cliente, id_pagamento, valor_total))

        conn.commit()

        id_venda = cursor.lastrowid

        cursor.close()
        conn.close()

        return id_venda
    
    @staticmethod
    def adicionar_detalhe_venda(id_venda, id_produto, qtd, preco):
        conn = Database.conectar()
        cursor = conn.cursor()

        sql = "INSERT INTO detalhe_vendas (id_produto, id_venda, qtd_produto, preco_unitario) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (id_produto, id_venda, qtd, preco))

        conn.commit()

        cursor.close()
        conn.close()