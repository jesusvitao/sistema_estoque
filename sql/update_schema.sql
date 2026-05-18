
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50)
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255),                        -- NULL para contas Google-only
    role_id INTEGER NOT NULL REFERENCES roles(id),
    google_id VARCHAR(255) UNIQUE                  -- Vinculação OAuth Google
);


CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria_id INT NOT NULL,
    tipo VARCHAR(50),
    frequencia VARCHAR(50),
	capacidade int,
	unidade_capacidade VARCHAR(10),
    especificacao VARCHAR(50),
    quantidade INT NOT NULL DEFAULT 0,
	unidade VARCHAR(10) DEFAULT 'unidade',
    estoque_minimo INT DEFAULT 20,
	observacao_produto TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE movimentacoes (
    id SERIAL PRIMARY KEY,
    produto_id INT NOT NULL,
	usuario_id INT NOT NULL,
    tipo_movimento VARCHAR(10) NOT NULL,
    quantidade INT NOT NULL,
    data_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
	FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

--inserção de Categorias
INSERT INTO categorias (nome) VALUES
('Memoria RAM'),
('SSD'),
('HD'),
('Cabo de vídeo'),
('Cabo de rede'),
('Material manutenção'),
('Ferramentas'),
('Periféricos'),
('Energia'),
('Componentes'),
('Equipamentos de rede'),
('Adaptadores'),
('Dispositivos');

--inserção das RAM 1
INSERT INTO produtos 
(nome, categoria_id, tipo, frequencia, capacidade, unidade_capacidade, especificacao, quantidade)
VALUES
('Memória RAM', 1, 'DDR3', 1333, 4, 'GB', 'Desktop', 2),
('Memória RAM', 1, 'DDR3', 1333, 8, 'GB', 'Desktop', 2),
('Memória RAM', 1, 'DDR3', 1600, 4, 'GB', 'Desktop', 4),
('Memória RAM', 1, 'DDR3', 1600, 8, 'GB', 'Desktop', 12),
('Memória RAM', 1, 'DDR3', 1600, 4, 'GB', 'Notebook', 18),
('Memória RAM', 1, 'DDR4', 2400, 4, 'GB', 'Desktop', 8),
('Memória RAM', 1, 'DDR4', 2400, 8, 'GB', 'Desktop', 5),
('Memória RAM', 1, 'DDR4', 2666, 4, 'GB', 'Desktop', 1),
('Memória RAM', 1, 'DDR4', 2666, 8, 'GB', 'Desktop', 6),
('Memória RAM', 1, 'DDR4', 1700, 8, 'GB', 'Notebook', 19)
('Memória RAM', 1, 'DDR4', 2666, 4, 'GB', 'Notebook', 1)
('Memória RAM', 1, 'DDR4', 3200, 4, 'GB', 'Notebook', 2)
('Memória RAM', 1, 'DDR4', 3200, 8, 'GB', 'Notebook', 25);

--inserção dos SSD's 2
INSERT INTO produtos(nome, categoria_id, capacidade, unidade_capacidade, especificacao, quantidade, estoque_minimo)
VALUES
('SSD', 2, 512, 'GB', 'M2', 1, 20),
('SSD', 2, 256, 'GB', 'M2', 47, 20),
('SSD', 2, 256, 'GB', 'SATA', 83, 20),
('SSD', 2, 512, 'GB', 'SATA', 5, 20

--inserção dos HD's 3
INSERT INTO produtos (nome, categoria_id, capacidade, unidade_capacidade, especificacao, quantidade)
VALUES
('HD', 3, 4, 'TB', 'Externo', 1),
('HD', 3, 500, 'GB', 'Desktop', 7),
('HD', 3, 1, 'TB', 'Desktop', 4),
('HD', 3, 160, 'GB', 'Desktop', 6),
('HD', 3, 80, 'GB', 'Desktop', 1),
('HD', 3, 2, 'TB', 'Desktop', 1),
('HD', 3, 1, 'TB', 'Notebook', 1);

--inserção dos Cabos de Vídeo 4
INSERT INTO produtos (nome, categoria_id, tipo, quantidade)
VALUES
('Cabo de vídeo', 4, 'HDMI', 17),
('Cabo de vídeo', 4, 'VGA', 7);

--inserção de Cabos de Rede 5
INSERT INTO produtos (nome, categoria_id, tipo, quantidade, unidade, observacao_produto)
VALUES
('Cabo de rede', 5, 'CAT6', 48, 'unidade', '1,5M'),
('Cabo de rede', 5, NULL, 1, 'caixa', 'Não recomendado para redes'),
('Cabo de rede', 5, NULL, 2, 'caixa', 'Avulsos'),
('Patch Panel', 5, NULL, 28, 'unidade', NULL),
('RJ45', 5, 'Fêmea', 3, 'caixa', NULL),
('RJ45', 5, 'Macho', 6, 'pacote', NULL),
('Tampa portas RJ45', 5, 'Fêmea', 1, 'caixa', NULL);

--inserção de Material de manutencao 6
INSERT INTO produtos (nome, categoria_id, especificacao, quantidade)
VALUES
('Abraçadeira de nilon', 6, 'pacote', 1),
('Alcool isopropílico', 6, NULL, 52),
('Limpa contato', 6, NULL, 14),
('Pasta térmica', 6, NULL, 242),
('Rolo de fita dupla face', 6, NULL, 20);

--inserção de Ferramentas 7
INSERT INTO produtos (nome, categoria_id, quantidade)
VALUES
('Alicate de bico', 7, 1),
('Alicate de crimpagem', 7, 14),
('Alicate normal', 7, 1),
('Chave de fenda', 7, 3),
('Chave philips', 7, 3),
('Chaves de impacto', 7, 5),
('Kit de pontas de chave notebook', 7, 1),
('Kit pontas parafusadeira', 7, 1),
('Kit de pinça', 7, 1),
('Kit de testador', 7, 4),
('Tesoura', 7, 1);

--inserção de Periféricos 8
INSERT INTO produtos (nome, categoria_id, especificacao, quantidade)
VALUES
('Headphone', 8, 'USB', 1),
('Mouse', 8, NULL, 14),
('Teclado', 8, NULL, 10);

--inserção de Energia 9
INSERT INTO produtos (nome, categoria_id, especificacao, quantidade)
VALUES
('Bateria de nobreak', 9, NULL, 16),
('Bateria de lítio', 9, NULL, 194),
('Cabo power', 9, NULL, 12),
('Cabo power', 9, 'POE', 12),
('Extenção para cabos de power', 9, NULL, 3),
('Nobreak', 9, NULL, 10),
('Soprador de ar', 9, NULL, 2);

--inserção de Componentes 10
INSERT INTO produtos (nome, categoria_id, tipo, especificacao, quantidade)
VALUES
('Cabo SATA', 10, NULL, NULL, 18),
('Cooler', 10, NULL, '27 Intel / 1 AMD', 54),
('CPU', 10, 'AMD', NULL, 1),
('CPU', 10, 'Intel', NULL, 3),
('Fonte', 10, NULL, NULL, 4),
('Placa de rede', 10, NULL, NULL, 25),
('Placa de vídeo', 10, NULL, NULL, 3);

--inserção de Equipamentos de rede 11
INSERT INTO produtos (nome, categoria_id, especificacao, quantidade)
VALUES
('Cabos SFP', 11, NULL, 29),
('MKV switch', 11, NULL, 6),
('Patch Panel', 11, NULL, 28),
('POE', 11, NULL, 2),
('Roteadores', 11, 'Intelbras', 15),
('Switch', 11, NULL, 16),
('Switch KVM', 11, '16 portas VGA', 2);

--inserção de Adaptadores 12
INSERT INTO produtos (nome, categoria_id, quantidade)
VALUES
('Adaptador de tomada', 12, 2),
('Adaptador HDMI', 12, 15);

--inserção de Adaptadores 13
INSERT INTO produtos (nome, categoria_id, especificacao, quantidade)
VALUES
('Caixa de cabos', 13, NULL, 1),
('Carregador', 13, 'Thin Client', 18),
('Doc station', 13, NULL, 3),
('Notebook', 13, NULL, 1);

--inserção de usuário
INSERT INTO roles (usuario)
VALUES ('admin');

--Permissão
INSERT INTO usuarios (nome, email, senha, role_id)
VALUES ('Admin', 'vitor.cba@outlook.com', '123456', 1);



-- Script SQL para atualização do esquema do banco de dados

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'produtos' AND column_name = 'descricao'
    ) THEN
        ALTER TABLE produtos
        ADD COLUMN descricao TEXT;
    END IF;
END
$$;

-- Adicionar a coluna 'preco' à tabela 'produtos' se ela não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'produtos' AND column_name = 'preco'
    ) THEN
        ALTER TABLE produtos
        ADD COLUMN preco NUMERIC(10, 2) DEFAULT 0.00;
    END IF;
END
$$;

-- Adicionar a coluna 'data_cadastro' à tabela 'produtos' se ela não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'produtos' AND column_name = 'data_cadastro'
    ) THEN
        ALTER TABLE produtos
        ADD COLUMN data_cadastro TIMESTAMP DEFAULT NOW();
    END IF;
END
$$;

-- Adicionar a coluna 'ativo' à tabela 'produtos' se ela não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'produtos' AND column_name = 'ativo'
    ) THEN
        ALTER TABLE produtos
        ADD COLUMN ativo BOOLEAN DEFAULT TRUE;
    END IF;
END
$$;

-- Inserir roles 'admin' e 'user' se não existirem
INSERT INTO roles (usuario)
SELECT 'admin'
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE usuario = 'admin');

INSERT INTO roles (usuario)
SELECT 'user'
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE usuario = 'user');

-- Atualizar produtos existentes para ter valores padrão para as novas colunas
UPDATE produtos SET descricao = COALESCE(descricao, '') WHERE descricao IS NULL;
UPDATE produtos SET preco = COALESCE(preco, 0.00) WHERE preco IS NULL;
UPDATE produtos SET data_cadastro = COALESCE(data_cadastro, NOW()) WHERE data_cadastro IS NULL;
UPDATE produtos SET ativo = COALESCE(ativo, TRUE) WHERE ativo IS NULL;
