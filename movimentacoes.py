from conexao import conectar

def registrar_movimentacao(produto_id, tipo_movimento, quantidade, usuario_id, observacao=None):
    conn = conectar()
    cursor = conn.cursor()
    try:
        conn.autocommit = False
        cursor.execute(
            "INSERT INTO movimentacoes (produto_id, tipo_movimento, quantidade, usuario_id, observacao) VALUES (%s, %s, %s, %s, %s)",
            (produto_id, tipo_movimento, quantidade, usuario_id, observacao)
        )
        if tipo_movimento == 'entrada':
            cursor.execute("UPDATE produtos SET quantidade = quantidade + %s WHERE id = %s", (quantidade, produto_id))
        elif tipo_movimento == 'saida':
            cursor.execute("UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s", (quantidade, produto_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.autocommit = True
        cursor.close()
        conn.close()

def listar_movimentacoes_por_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, p.nome, m.tipo_movimento, m.quantidade, m.data_movimento, u.email, m.observacao
        FROM movimentacoes m
        JOIN produtos p ON m.produto_id = p.id
        JOIN usuarios u ON m.usuario_id = u.id
        WHERE m.produto_id = %s
        ORDER BY m.data_movimento DESC
    """, (produto_id,))
    movimentacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return movimentacoes

def listar_todas_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, p.nome, m.tipo_movimento, m.quantidade, m.data_movimento, u.email, m.observacao
        FROM movimentacoes m
        JOIN produtos p ON m.produto_id = p.id
        JOIN usuarios u ON m.usuario_id = u.id
        ORDER BY m.data_movimento DESC
    """)
    movimentacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return movimentacoes
