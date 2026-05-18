# Sistema de Controle de Estoque 

Um sistema web completo de gestão de estoque desenvolvido em **Flask** com **PostgreSQL**, permitindo controle total de produtos, movimentações de estoque e geração de relatórios.

## Funcionalidades

- **Autenticação de Usuários:** Login seguro com email e senha, com suporte a login via Google (OAuth 2.0)
- **Gestão de Produtos:** Cadastro, edição e exclusão lógica de produtos com filtro e pesquisa em tempo real
- **Gestão de Categorias:** Cadastro, edição e exclusão de categorias de produtos
- **Movimentação de Estoque:** Registro de entradas e saídas com histórico completo
- **Controle de Permissões:** Diferenciação entre usuários administradores (admin) e comuns (user)
- **Alerta de Estoque Mínimo:** Produtos abaixo do estoque mínimo são destacados visualmente
- **Relatórios:** Geração de relatório de estoque atual com exportação em Excel (.xlsx) e relatório de movimentações
- **Interface Responsiva:** Design moderno com Bootstrap

## Tecnologias Utilizadas

- **Backend:** Python com Flask
- **Banco de Dados:** PostgreSQL (Neon)
- **Frontend:** HTML5, CSS3, Bootstrap 4
- **Bibliotecas:** psycopg2 (conexão com PostgreSQL), Pandas (relatórios), openpyxl (exportação XLSX), google-auth (verificação OAuth 2.0)
- **Hospedagem:** Render com Git

## Deploy

O sistema pode ser hospedado na plataforma Render.

Configurações utilizadas:

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn main:app --bind 0.0.0.0:$PORT

## Funcionamento

### 1. Ferramentas
- Python 3.7+
- PostgreSQL (ou Neon)
- pip (gerenciador de pacotes Python)

### 2. Clonar o Repositório

```bash
git clone <seu-repositorio>
cd sistema_estoque
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Conexão com o Banco de Dados

Edite o arquivo `conexao.py` e configure as credenciais do seu banco de dados:

```python
DB_HOST = "host_neon"
DB_PORT = 5432
DB_NAME = "estoque_ti"
DB_USER = "usuario_neon"
DB_PASSWORD = "senha_neon"
```

### 5. Configurar Variáveis de Ambiente

Configure as seguintes variáveis antes de iniciar o sistema:

```bash
SECRET_KEY=uma_chave_secreta_longa_e_aleatoria
GOOGLE_CLIENT_ID=seu_client_id.apps.googleusercontent.com
```

### 6. Configurar Login com Google (OAuth 2.0)

- Acesse console.cloud.google.com e crie um projeto
- Vá em APIs e Serviços > Credenciais > Criar credencial > ID do cliente OAuth
- Selecione o tipo: Aplicação da Web
- Adicione em Origens JavaScript autorizadas: http://localhost:5000
- Copie o Client ID gerado e defina na variável de ambiente GOOGLE_CLIENT_ID

Ao fazer login com o Google, se o e-mail já existir no banco, o Google ID é vinculado à conta existente. Novos usuários são criados automaticamente com perfil user.

## Estrutura do Projeto

```
sistema_estoque/
├── main.py                    # Arquivo principal com rotas Flask
├── conexao.py                 # Configuração de conexão com o banco
├── banco.py                   # Funções genéricas de banco de dados
├── users.py                   # Lógica de autenticação e OAuth
├── produtos.py                # CRUD de produtos e categorias
├── movimentacoes.py           # Lógica de movimentação de estoque
├── relatorios.py              # Geração de relatórios com Pandas e XLSX
├── requirements.txt           # Dependências do projeto
├── README.md                  # Este arquivo
├── templates/                 # Templates HTML
│   ├── login.html
│   ├── dashboard.html
│   ├── produtos.html
│   ├── produto_form.html
│   ├── categorias.html
│   ├── categoria_form.html
│   ├── movimentar_estoque.html
│   ├── historico_movimentacoes.html
│   ├── relatorio_movimentacoes.html
│   ├── relatorio_estoque_atual.html
│   ├── usuarios.html
│   ├── usuario_form.html
│   ├── erro_404.html
│   └── erro_500.html
├── static/                    # Arquivos estáticos
│   └── CSS/
│       └── style.css
└── sql/                       # Scripts SQL
    └── update_schema.sql
```

## Perfis de Acesso

O sistema possui dois perfis de acesso:

**admin** tem acesso completo ao sistema, podendo listar, adicionar, editar e deletar produtos, movimentar estoque, visualizar histórico, gerar relatórios, gerenciar usuários e categorias.

**user** tem acesso limitado, podendo listar produtos, visualizar o histórico de movimentações e consultar o relatório de estoque atual com exportação em XLSX.

## Segurança

- **Senhas:** Armazenadas em texto simples (para desenvolvimento). Em produção, use hash (bcrypt, argon2)
- **Chave Secreta:** Defina `SECRET_KEY` como variável de ambiente, nunca hardcode no código
- **Google OAuth:** Defina `GOOGLE_CLIENT_ID` como variável de ambiente
- **Debug:** Nunca use `debug=True` em produção
- **HTTPS:** Use HTTPS em produção

## Fluxo de Uso

1. **Login:** Acesse a página de login e insira suas credenciais ou use o botão Entrar com Google
2. **Dashboard:** Após login, você verá o menu principal com as opções disponíveis para o seu perfil
3. **Gerenciar Produtos:** Adicione, edite ou delete produtos e utilize o filtro para localizar itens
4. **Movimentar Estoque:** Registre entradas e saídas de produtos (somente admin)
5. **Visualizar Relatórios:** Consulte o estoque atual e exporte em XLSX, ou visualize o histórico de movimentações
6. **Logout:** Clique em "Sair" para encerrar a sessão

## Relatórios

O sistema gera dois tipos de relatórios:

- **Relatório de Movimentações:** Lista todas as entradas e saídas de estoque (somente admin)
- **Relatório de Estoque Atual:** Mostra a situação atual de todos os produtos com opção de exportação em XLSX formatado, disponível para admin e user

## Solução de Problemas

### Erro de Conexão com o Banco

- Verifique as credenciais em `conexao.py`
- Certifique-se de que o servidor PostgreSQL está ativo
- Verifique se o IP está na lista de permissões do Neon

### Login com Google não funciona

- Confirme que GOOGLE_CLIENT_ID está configurado corretamente
- Verifique se http://localhost:5000 está em Origens JavaScript autorizadas no console do Google

### Acesso Limitado após login

- O perfil do usuário no banco deve ser exatamente `admin` ou `user` (minúsculo)
- Verifique executando no banco: `SELECT id, usuario FROM roles;`

### Erro 404 ou 500

- Verifique os logs do Flask no terminal
- Certifique-se de que todos os templates estão na pasta `templates/`

## Objetivo

Este projeto é fornecido como está para fins educacionais, foi desenvolvido como projeto acadêmico / estágio supervisionado.
