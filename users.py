from banco import buscar_usuario_por_email, buscar_role_por_id
from conexao import conectar

def autenticar_usuario(email, senha):
    usuario = buscar_usuario_por_email(email)

    if not usuario:
        return None

    senha_banco = usuario[3]

    if senha_banco and senha_banco == senha:
        role = buscar_role_por_id(usuario[4])
        if role:
            return {
                "id": usuario[0],
                "nome": usuario[1],
                "email": usuario[2],
                "role": role[1]
            }

    return None

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.nome, u.email, u.role_id, r.usuario
        FROM usuarios u
        LEFT JOIN roles r ON u.role_id = r.id
        ORDER BY u.nome
    """)
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios

def buscar_usuario_por_id(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.nome, u.email, u.role_id, r.usuario
        FROM usuarios u
        LEFT JOIN roles r ON u.role_id = r.id
        WHERE u.id = %s
    """, (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

def criar_usuario(nome, email, senha, role_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, role_id) VALUES (%s, %s, %s, %s) RETURNING id",
        (nome, email, senha, role_id)
    )
    novo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return novo_id

def atualizar_usuario(usuario_id, nome, email, role_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET nome = %s, email = %s, role_id = %s WHERE id = %s",
        (nome, email, role_id, usuario_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def atualizar_senha_usuario(usuario_id, nova_senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET senha = %s WHERE id = %s", (nova_senha, usuario_id))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
    conn.commit()
    cursor.close()
    conn.close()

def listar_roles():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario FROM roles ORDER BY usuario")
    roles = cursor.fetchall()
    cursor.close()
    conn.close()
    return roles

def criar_ou_atualizar_usuario_google(google_id, email, nome):
    """
    Busca ou cria um usuário pelo google_id.
    Se o email já existe, vincula o google_id a ele.
    Novos usuários recebem a role 'usuario' por padrão.
    Retorna dict com id, nome e role.
    """
    conn = conectar()
    cursor = conn.cursor()

    # Tenta achar pelo google_id
    cursor.execute("SELECT u.id, u.nome, r.usuario FROM usuarios u LEFT JOIN roles r ON u.role_id = r.id WHERE u.google_id = %s", (google_id,))
    usuario = cursor.fetchone()
    if usuario:
        cursor.close()
        conn.close()
        return {"id": usuario[0], "nome": usuario[1], "role": usuario[2]}

    # Tenta achar pelo email (vincula google_id)
    cursor.execute("SELECT u.id, u.nome, r.usuario FROM usuarios u LEFT JOIN roles r ON u.role_id = r.id WHERE u.email = %s", (email,))
    usuario = cursor.fetchone()
    if usuario:
        cursor.execute("UPDATE usuarios SET google_id = %s WHERE email = %s", (google_id, email))
        conn.commit()
        cursor.close()
        conn.close()
        return {"id": usuario[0], "nome": usuario[1], "role": usuario[2]}

    # Cria novo usuário com a role não-admin do banco (seja 'user', 'usuario', etc)
    cursor.execute("SELECT id, usuario FROM roles WHERE usuario != 'admin' ORDER BY id LIMIT 1")
    role = cursor.fetchone()
    role_id = role[0] if role else 2
    role_name = role[1] if role else "user"

    cursor.execute(
        "INSERT INTO usuarios (nome, email, google_id, role_id) VALUES (%s, %s, %s, %s) RETURNING id",
        (nome, email, google_id, role_id)
    )
    novo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"id": novo_id, "nome": nome, "role": role_name}
