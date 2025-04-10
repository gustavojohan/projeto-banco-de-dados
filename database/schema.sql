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