from conexao import conectar

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.nome, p.descricao, p.quantidade, p.data_cadastro, p.ativo, 
               c.nome as categoria, p.tipo, p.frequencia, p.capacidade, 
               p.unidade_capacidade, p.especificacao, p.unidade, p.estoque_minimo
        FROM produtos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        ORDER BY p.nome
    """)
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return produtos

def buscar_produto_por_id(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.nome, p.descricao, p.quantidade, p.data_cadastro, p.ativo,
               p.categoria_id, p.tipo, p.frequencia, p.capacidade, 
               p.unidade_capacidade, p.especificacao, p.unidade, p.estoque_minimo
        FROM produtos p
        WHERE p.id = %s
    """, (produto_id,))
    produto = cursor.fetchone()
    cursor.close()
    conn.close()
    return produto

def adicionar_produto(nome, descricao, quantidade, categoria_id, especificacao, unidade, estoque_minimo, ativo=True):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, descricao, quantidade, categoria_id, 
                             especificacao, unidade, estoque_minimo, ativo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (nome, descricao, quantidade, categoria_id, especificacao, unidade, estoque_minimo, ativo))
    novo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return novo_id

def atualizar_produto(produto_id, nome, descricao, quantidade, categoria_id, especificacao, unidade, estoque_minimo, ativo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos 
        SET nome = %s, descricao = %s, quantidade = %s, categoria_id = %s,
            especificacao = %s, unidade = %s, estoque_minimo = %s, ativo = %s
        WHERE id = %s
    """, (nome, descricao, quantidade, categoria_id, especificacao, unidade, estoque_minimo, ativo, produto_id))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET ativo = FALSE WHERE id = %s", (produto_id,))
    conn.commit()
    cursor.close()
    conn.close()

def listar_categorias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM categorias ORDER BY nome")
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return categorias

def criar_categoria(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categorias (nome) VALUES (%s) RETURNING id", (nome,))
    novo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return novo_id

def atualizar_categoria(categoria_id, nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE categorias SET nome = %s WHERE id = %s", (nome, categoria_id))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_categoria(categoria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE id = %s", (categoria_id,))
    conn.commit()
    cursor.close()
    conn.close()
