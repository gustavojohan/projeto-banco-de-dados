CREATE DATABASE IF NOT EXISTS distribuidora;
USE distribuidora;


CREATE TABLE IF NOT EXISTS estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    preco DECIMAL(10, 2) NOT NULL,
    quantidade INT NOT NULL DEFAULT 0,
    categoria VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS pessoas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf_cnpj VARCHAR(18) UNIQUE,
    endereco VARCHAR(100),
    telefone VARCHAR(11),
    email VARCHAR(100) UNIQUE,
    senha VARCHAR(20),
    tipo ENUM('cliente', 'funcionario', 'admin') NOT NULL
);

CREATE TABLE IF NOT EXISTS formas_pagamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao VARCHAR(100)
);

INSERT INTO formas_pagamento (nome, descricao) VALUES
('pix', 'Pagamento via PIX'),
('boleto', 'Pagamento via Boleto'),
('cartao', 'Cartão');

CREATE TABLE IF NOT EXISTS vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_funcionario INT,
    id_pagamento INT,
    data_solicitacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_processamento DATETIME,
    status ENUM('solicitado', 'processando', 'concluido', 'cancelado') DEFAULT 'solicitado',
    valor_total DECIMAL(10, 2),
    FOREIGN KEY (id_cliente) REFERENCES pessoas(id) ON DELETE SET NULL, 
    FOREIGN KEY (id_funcionario) REFERENCES pessoas(id) ON DELETE SET NULL,
    FOREIGN KEY (id_pagamento) REFERENCES formas_pagamento(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS detalhe_vendas (
    id_produto INT,
    id_venda INT,
    qtd_produto INT NOT NULL DEFAULT 0,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    desconto DECIMAL(10, 2) DEFAULT 0.00,
    PRIMARY KEY (id_produto, id_venda),
    FOREIGN KEY (id_produto) REFERENCES estoque(id) ON DELETE CASCADE,
    FOREIGN KEY (id_venda) REFERENCES vendas(id) ON DELETE CASCADE
);

CREATE OR REPLACE VIEW vw_produtos_disponiveis AS
SELECT id, nome, preco, quantidade, categoria
FROM estoque;

CREATE OR REPLACE VIEW vw_detalhes_vendas_funcionario AS
SELECT
    v.id AS id_venda,
    v.data_solicitacao,
    v.data_processamento,
    v.status,
    v.valor_total,

    f.id AS id_funcionario,
    f.nome AS nome_funcionario,

    c.id AS id_cliente,
    c.nome AS nome_cliente,

    p.id AS id_produto,
    p.nome AS nome_produto,
    dv.qtd_produto,
    dv.preco_unitario,
    dv.desconto,

    dv.qtd_produto * (dv.preco_unitario - dv.desconto) AS subtotal_com_desconto

FROM vendas v
JOIN pessoas f ON v.id_funcionario = f.id AND f.tipo = 'funcionario'
JOIN pessoas c ON v.id_cliente = c.id AND c.tipo = 'cliente'
JOIN detalhe_vendas dv ON dv.id_venda = v.id
JOIN estoque p ON p.id = dv.id_produto;