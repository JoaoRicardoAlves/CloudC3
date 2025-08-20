-- Sistema de Gerenciamento de Biblioteca
-- Script SQL para criação das tabelas e relacionamentos
-- Banco de Dados: PostgreSQL

-- Criação da tabela de Autores
CREATE TABLE IF NOT EXISTS autores (
    id_autor SERIAL PRIMARY KEY,
    nome_autor VARCHAR(100) NOT NULL,
    nacionalidade VARCHAR(50),
    data_nascimento DATE,
    biografia TEXT
);

-- Criação da tabela de Livros
CREATE TABLE IF NOT EXISTS livros (
    id_livro SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    id_autor INTEGER NOT NULL,
    genero VARCHAR(50) NOT NULL,
    ano_publicacao INTEGER,
    preco DECIMAL(10,2) NOT NULL,
    quantidade_estoque INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (id_autor) REFERENCES autores(id_autor)
);

-- Criação da tabela de Pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido SERIAL PRIMARY KEY,
    data_pedido DATE NOT NULL DEFAULT CURRENT_DATE,
    nome_cliente VARCHAR(100) NOT NULL,
    email_cliente VARCHAR(100),
    valor_total DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

-- Criação da tabela de Itens do Pedido (relacionamento N:N entre Pedidos e Livros)
CREATE TABLE IF NOT EXISTS itens_pedido (
    id_item SERIAL PRIMARY KEY,
    id_pedido INTEGER NOT NULL,
    id_livro INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_livro) REFERENCES livros(id_livro)
);

-- Inserção de dados de exemplo
INSERT INTO autores (nome_autor, nacionalidade, data_nascimento, biografia) VALUES
('Machado de Assis', 'Brasileira', '1839-06-21', 'Escritor brasileiro, considerado um dos maiores nomes da literatura nacional'),
('Clarice Lispector', 'Brasileira', '1920-12-10', 'Escritora e jornalista brasileira nascida na Ucrânia'),
('José Saramago', 'Portuguesa', '1922-11-16', 'Escritor português, Prêmio Nobel de Literatura'),
('Gabriel García Márquez', 'Colombiana', '1927-03-06', 'Escritor colombiano, Prêmio Nobel de Literatura');

INSERT INTO livros (titulo, id_autor, genero, ano_publicacao, preco, quantidade_estoque) VALUES
('Dom Casmurro', 1, 'Romance', 1899, 25.90, 15),
('O Cortiço', 1, 'Romance', 1890, 22.50, 8),
('A Hora da Estrela', 2, 'Romance', 1977, 28.00, 12),
('Água Viva', 2, 'Romance', 1973, 24.90, 6),
('Ensaio sobre a Cegueira', 3, 'Romance', 1995, 32.00, 10),
('O Evangelho Segundo Jesus Cristo', 3, 'Romance', 1991, 29.90, 7),
('Cem Anos de Solidão', 4, 'Realismo Mágico', 1967, 35.00, 20),
('O Amor nos Tempos do Cólera', 4, 'Romance', 1985, 31.50, 9);

INSERT INTO pedidos (data_pedido, nome_cliente, email_cliente, valor_total) VALUES
('2024-01-15', 'João Silva', 'joao@email.com', 51.80),
('2024-01-20', 'Maria Santos', 'maria@email.com', 64.00),
('2024-02-01', 'Pedro Oliveira', 'pedro@email.com', 35.00);

INSERT INTO itens_pedido (id_pedido, id_livro, quantidade, preco_unitario, subtotal) VALUES
(1, 1, 2, 25.90, 51.80),
(2, 3, 1, 28.00, 28.00),
(2, 5, 1, 32.00, 32.00),
(2, 8, 1, 31.50, 31.50),
(3, 7, 1, 35.00, 35.00);

-- Atualização dos valores totais dos pedidos
UPDATE pedidos SET valor_total = 51.80 WHERE id_pedido = 1;
UPDATE pedidos SET valor_total = 91.50 WHERE id_pedido = 2;
UPDATE pedidos SET valor_total = 35.00 WHERE id_pedido = 3;