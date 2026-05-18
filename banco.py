from conexao import conectar

def buscar_usuario_por_email(email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, email, senha, role_id, google_id FROM usuarios WHERE email = %s",
        (email,)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

def buscar_role_por_id(role_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario FROM roles WHERE id = %s", (role_id,))
    role = cursor.fetchone()
    cursor.close()
    conn.close()
    return role
