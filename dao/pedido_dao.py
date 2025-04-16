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
    def adicionar_detalhe_venda(id_venda, id_produto, qtd, preco_unitario, desconto):
        conn = Database.conectar()
        cursor = conn.cursor()

        sql = "INSERT INTO detalhe_vendas (id_produto, id_venda, qtd_produto, preco_unitario, desconto) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (id_produto, id_venda, qtd, preco_unitario, desconto))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def historico_compras(id_cliente):
        conn = Database.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, valor_total, status, data_solicitacao
            FROM vendas
            WHERE id_cliente = %s
            ORDER BY data_solicitacao DESC
        """, (id_cliente,))
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado
    
    @staticmethod
    def listar_pedidos_em_analise():
        conn = Database.conectar()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT v.id, p.nome AS cliente, v.valor_total, v.data_solicitacao
            FROM vendas v
            JOIN pessoas p ON v.id_cliente = p.id
            WHERE v.status = 'solicitado'
        """
        cursor.execute(sql)
        pedidos = cursor.fetchall()

        cursor.close()
        conn.close()

        return pedidos
    
    @staticmethod
    def atualizar_status_pedido(id_venda, novo_status, id_funcionario):
        conn = Database.conectar()
        cursor = conn.cursor()

        sql = "UPDATE vendas SET status = %s, id_funcionario = %s, data_processamento = NOW() WHERE id = %s"
        cursor.execute(sql, (novo_status, id_funcionario, id_venda))
        conn.commit()

        cursor.close()
        conn.close()
    
    @staticmethod
    def buscar_detalhes_vendas():
        conn = Database.conectar()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM vw_detalhes_vendas_funcionario"
        cursor.execute(sql)
        tabela_vendas = cursor.fetchall()

        cursor.close()
        conn.close()
        return tabela_vendas
    
    @staticmethod
    def get_detalhes_venda(id_venda):
        conn = Database.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_produto, qtd_produto
            FROM detalhe_vendas
            WHERE id_venda = %s
        """, (id_venda,))
        resultados = cursor.fetchall()
        conn.close()
        return [{"id_produto": row[0], "qtd_produto": row[1]} for row in resultados]