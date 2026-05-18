from flask import Flask, render_template, request, session, redirect, url_for, flash, send_file, jsonify
from werkzeug.security import generate_password_hash
from flask import session, flash, redirect, url_for, request, render_template
from users import autenticar_usuario, listar_usuarios, buscar_usuario_por_id, criar_usuario, atualizar_usuario, atualizar_senha_usuario, deletar_usuario, listar_roles, criar_ou_atualizar_usuario_google
from produtos import listar_produtos, adicionar_produto, buscar_produto_por_id, atualizar_produto, deletar_produto, listar_categorias, criar_categoria, atualizar_categoria, deletar_categoria
from movimentacoes import registrar_movimentacao, listar_movimentacoes_por_produto, listar_todas_movimentacoes
from relatorios import gerar_relatorio_movimentacoes, gerar_relatorio_estoque_atual, gerar_relatorio_estoque_xlsx, gerar_relatorio_movimentacoes_xlsx
from functools import wraps
from io import BytesIO
from datetime import timedelta
import os
import google.auth.transport.requests
from google.oauth2 import id_token

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave_local_dev")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "SEU_CLIENT_ID_AQUI")

# ==================== Decoradores ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Você precisa estar logado para acessar esta página.", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "usuario_id" not in session:
                flash("Você precisa estar logado para acessar esta página.", "danger")
                return redirect(url_for("login"))
            if session.get("usuario_role") not in roles:
                flash("Acesso negado.", "danger")
                return redirect(url_for("dashboard"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

#====================== Senhas Alter =========================

@app.route('/admin/alterar_senha/<int:id_usuario>', methods=['GET', 'POST'])
def alterar_senha_usuario(id_usuario):
    if 'usuario_id' not in session:
        flash('Você precisa estar logado.', 'danger')
        return redirect(url_for('login'))

    if session.get('usuario_role') != 'admin':
        flash('Acesso negado. Apenas administradores podem alterar senhas.', 'danger')
        return redirect(url_for('dashboard'))

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email
        FROM usuarios
        WHERE id = %s
    """, (id_usuario,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        conn.close()
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('usuarios'))

    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')

        if nova_senha != confirmar_senha:
            cursor.close()
            conn.close()
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('alterar_senha_usuario', id_usuario=id_usuario))

        senha_hash = generate_password_hash(nova_senha)

        cursor.execute("""
            UPDATE usuarios
            SET senha = %s
            WHERE id = %s
        """, (senha_hash, id_usuario))

        conn.commit()
        cursor.close()
        conn.close()

        flash('Senha alterada com sucesso.', 'success')
        return redirect(url_for('usuarios'))

    cursor.close()
    conn.close()

    return render_template('alterar_senha_usuario.html', usuario=usuario)

# ==================== Autenticação ====================

@app.route("/")
def index():
    if "usuario_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    email_digitado = None
    if request.method == "POST":
        email_digitado = request.form["email"]
        usuario = autenticar_usuario(email_digitado, request.form["senha"])
        if usuario:
            session.permanent = True
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            session["usuario_role"] = usuario["role"]
            flash(f"Bem-vindo, {usuario['nome']}!", "success")
            return redirect(url_for("dashboard"))
        erro = "Email ou senha inválidos. Tente novamente."
    return render_template("login.html", erro=erro, email_digitado=email_digitado, google_client_id=GOOGLE_CLIENT_ID)

@app.route("/auth/google", methods=["POST"])
def auth_google():
    try:
        data = request.get_json()
        credential = data.get("credential")
        id_info = id_token.verify_oauth2_token(
            credential,
            google.auth.transport.requests.Request(),
            GOOGLE_CLIENT_ID
        )
        google_id = id_info["sub"]
        email = id_info["email"]
        nome = id_info.get("name", email)
        usuario = criar_ou_atualizar_usuario_google(google_id, email, nome)
        session.permanent = True
        session["usuario_id"] = usuario["id"]
        session["usuario_nome"] = usuario["nome"]
        session["usuario_role"] = usuario["role"]
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/logout")
def logout():
    session.clear()
    flash("Você foi desconectado com sucesso.", "info")
    return redirect(url_for("login"))

# ==================== Dashboard ====================

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", nome=session["usuario_nome"])

# ==================== Produtos ====================

@app.route("/produtos")
@login_required
@role_required("admin", "user")
def produtos():
    return render_template("produtos.html", produtos=listar_produtos())

@app.route("/produto/novo", methods=["GET", "POST"])
@login_required
@role_required("admin")
def novo_produto():
    categorias = listar_categorias()
    if request.method == "POST":
        try:
            adicionar_produto(
                request.form["nome"],
                request.form["descricao"],
                int(request.form["quantidade"]),
                int(request.form["categoria_id"]),
                request.form["especificacao"],
                request.form["unidade"],
                int(request.form["estoque_minimo"]),
                ativo=request.form.get("ativo") == "on"
            )
            flash("Produto adicionado com sucesso!", "success")
            return redirect(url_for("produtos"))
        except Exception as e:
            flash(f"Erro ao adicionar produto: {e}", "danger")
    return render_template("produto_form.html", categorias=categorias)

@app.route("/produto/editar/<int:produto_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def editar_produto(produto_id):
    produto = buscar_produto_por_id(produto_id)
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("produtos"))
    if request.method == "POST":
        try:
            atualizar_produto(
                produto_id,
                request.form["nome"],
                request.form["descricao"],
                int(request.form["quantidade"]),
                int(request.form["categoria_id"]),
                request.form["especificacao"],
                request.form["unidade"],
                int(request.form["estoque_minimo"]),
                ativo=request.form.get("ativo") == "on"
            )
            flash("Produto atualizado com sucesso!", "success")
            return redirect(url_for("produtos"))
        except Exception as e:
            flash(f"Erro ao atualizar produto: {e}", "danger")
    return render_template("produto_form.html", produto=produto, categorias=listar_categorias())

@app.route("/produto/deletar/<int:produto_id>", methods=["POST"])
@login_required
@role_required("admin")
def deletar_produto_route(produto_id):
    try:
        deletar_produto(produto_id)
        flash("Produto deletado com sucesso!", "info")
    except Exception as e:
        flash(f"Erro ao deletar produto: {e}", "danger")
    return redirect(url_for("produtos"))

# ==================== Movimentações ====================

@app.route("/movimentar_estoque/<int:produto_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def movimentar_estoque(produto_id):
    produto = buscar_produto_por_id(produto_id)
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("produtos"))
    if request.method == "POST":
        try:
            tipo = request.form["tipo_movimento"]
            qtd = int(request.form["quantidade"])
            registrar_movimentacao(produto_id, tipo, qtd, session["usuario_id"], request.form.get("observacao", ""))
            flash(f"Movimentação de {tipo} de {qtd} unidades para {produto[1]} registrada com sucesso!", "success")
            return redirect(url_for("produtos"))
        except Exception as e:
            flash(f"Erro ao registrar movimentação: {e}", "danger")
    return render_template("movimentar_estoque.html", produto=produto)

@app.route("/historico_movimentacoes")
@login_required
@role_required("admin", "user")
def historico_movimentacoes():
    return render_template("historico_movimentacoes.html", movimentacoes=listar_todas_movimentacoes())

# ==================== Relatórios ====================

@app.route("/relatorio/movimentacoes")
@login_required
@role_required("admin")
def relatorio_movimentacoes():
    try:
        tabela_html = gerar_relatorio_movimentacoes().to_html(classes="table table-striped", index=False)
        return render_template("relatorio_movimentacoes.html", tabela_html=tabela_html)
    except Exception as e:
        flash(f"Erro ao gerar relatório: {e}", "danger")
        return redirect(url_for("dashboard"))

@app.route("/relatorio/movimentacoes/xlsx")
@login_required
@role_required("admin")
def relatorio_movimentacoes_xlsx():
    try:
        output = gerar_relatorio_movimentacoes_xlsx()
        return send_file(output, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         as_attachment=True, download_name="relatorio_movimentacoes.xlsx")
    except Exception as e:
        flash(f"Erro ao exportar relatório: {e}", "danger")
        return redirect(url_for("relatorio_movimentacoes"))

@app.route("/relatorio/estoque_atual")
@login_required
@role_required("admin", "user")
def relatorio_estoque_atual():
    try:
        tabela_html = gerar_relatorio_estoque_atual().to_html(classes="table table-striped", index=False)
        return render_template("relatorio_estoque_atual.html", tabela_html=tabela_html)
    except Exception as e:
        flash(f"Erro ao gerar relatório: {e}", "danger")
        return redirect(url_for("dashboard"))

@app.route("/relatorio/estoque_atual/xlsx")
@login_required
@role_required("admin", "user")
def relatorio_estoque_atual_xlsx():
    try:
        output = gerar_relatorio_estoque_xlsx()
        return send_file(output, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         as_attachment=True, download_name="relatorio_estoque_atual.xlsx")
    except Exception as e:
        flash(f"Erro ao exportar relatório: {e}", "danger")
        return redirect(url_for("relatorio_estoque_atual"))

# ==================== Usuários ====================

@app.route("/usuarios")
@login_required
@role_required("admin")
def usuarios():
    return render_template("usuarios.html", usuarios=listar_usuarios())

@app.route("/usuario/novo", methods=["GET", "POST"])
@login_required
@role_required("admin")
def novo_usuario():
    roles = listar_roles()
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            criar_usuario(nome, request.form["email"], request.form["senha"], int(request.form["role_id"]))
            flash(f"Usuario {nome} criado com sucesso!", "success")
            return redirect(url_for("usuarios"))
        except Exception as e:
            flash(f"Erro ao criar usuario: {e}", "danger")
    return render_template("usuario_form.html", roles=roles)

@app.route("/usuario/editar/<int:usuario_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def editar_usuario_route(usuario_id):
    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        flash("Usuario nao encontrado.", "danger")
        return redirect(url_for("usuarios"))
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            atualizar_usuario(usuario_id, nome, request.form["email"], int(request.form["role_id"]))
            nova_senha = request.form.get("nova_senha", "").strip()
            if nova_senha:
                atualizar_senha_usuario(usuario_id, nova_senha)
            flash(f"Usuario {nome} atualizado com sucesso!", "success")
            return redirect(url_for("usuarios"))
        except Exception as e:
            flash(f"Erro ao atualizar usuario: {e}", "danger")
    return render_template("usuario_form.html", usuario=usuario, roles=listar_roles())

@app.route("/usuario/deletar/<int:usuario_id>", methods=["POST"])
@login_required
@role_required("admin")
def deletar_usuario_route(usuario_id):
    try:
        usuario = buscar_usuario_por_id(usuario_id)
        if usuario:
            deletar_usuario(usuario_id)
            flash("Usuario deletado com sucesso!", "info")
        else:
            flash("Usuario nao encontrado.", "danger")
    except Exception as e:
        flash(f"Erro ao deletar usuario: {e}", "danger")
    return redirect(url_for("usuarios"))

# ==================== Categorias ====================

@app.route("/categorias")
@login_required
@role_required("admin")
def categorias():
    return render_template("categorias.html", categorias=listar_categorias())

@app.route("/categoria/nova", methods=["GET", "POST"])
@login_required
@role_required("admin")
def nova_categoria():
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            criar_categoria(nome)
            flash(f"Categoria {nome} criada com sucesso!", "success")
            return redirect(url_for("categorias"))
        except Exception as e:
            flash(f"Erro ao criar categoria: {e}", "danger")
    return render_template("categoria_form.html")

@app.route("/categoria/editar/<int:categoria_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def editar_categoria_route(categoria_id):
    categorias_list = listar_categorias()
    categoria = next((c for c in categorias_list if c[0] == categoria_id), None)
    if not categoria:
        flash("Categoria nao encontrada.", "danger")
        return redirect(url_for("categorias"))
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            atualizar_categoria(categoria_id, nome)
            flash("Categoria atualizada com sucesso!", "success")
            return redirect(url_for("categorias"))
        except Exception as e:
            flash(f"Erro ao atualizar categoria: {e}", "danger")
    return render_template("categoria_form.html", categoria=categoria)

@app.route("/categoria/deletar/<int:categoria_id>", methods=["POST"])
@login_required
@role_required("admin")
def deletar_categoria_route(categoria_id):
    try:
        deletar_categoria(categoria_id)
        flash("Categoria deletada com sucesso!", "info")
    except Exception as e:
        flash(f"Erro ao deletar categoria: {e}", "danger")
    return redirect(url_for("categorias"))

# ==================== Erros ====================

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template("erro_404.html"), 404

@app.errorhandler(500)
def erro_interno(e):
    return render_template("erro_500.html"), 500

# ==================== Execução ====================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
