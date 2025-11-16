import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

# Configuração do Flask
app = Flask(__name__)
# Chave secreta obrigatória para sessões e mensagens flash
# Mantenha esta chave segura em um ambiente de produção!
app.secret_key = 'sua_chave_secreta_aqui_para_sessao'

# Configuração do Banco de Dados
DATABASE = 'banco.db'

# Funções auxiliares para o banco de dados
def get_db():
    """Obtém a conexão com o banco de dados. Usa 'g' para reutilizar a conexão."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Configura o db para retornar linhas como dicionários, acessíveis por nome
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Fecha a conexão com o banco de dados ao final da requisição."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Cria as tabelas do banco de dados se elas não existirem."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Criação da tabela 'usuario'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            );
        ''')
        
        # Criação da tabela 'tarefa'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tarefa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                titulo TEXT NOT NULL,
                descricao TEXT,
                FOREIGN KEY(usuario_id) REFERENCES usuario(id)
            );
        ''')
        db.commit()

# --- Rotas de Autenticação e Navegação ---

@app.route('/')
def index():
    """Página inicial com links para login e cadastro."""
    # Se o usuário já estiver logado, redireciona para o dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """Rota para o cadastro de novos usuários."""
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        db = get_db()
        cursor = db.cursor()
        
        try:
            # DESAFIO EXTRA: Criptografia de Senha
            # Gera o hash da senha antes de armazenar
            senha_hash = generate_password_hash(senha)
            
            cursor.execute(
                "INSERT INTO usuario (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha_hash)
            )
            db.commit()
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            # Erro de integridade: provavelmente email duplicado
            flash('Erro: O e-mail já está em uso. Tente outro.', 'danger')
            return render_template('cadastro.html', nome=nome, email=email)
        except Exception as e:
            flash(f'Erro ao cadastrar: {e}', 'danger')
            return render_template('cadastro.html', nome=nome, email=email)

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Rota para o login de usuários."""
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT id, nome, senha FROM usuario WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        
        if usuario:
            # Verifica a senha criptografada
            if check_password_hash(usuario['senha'], senha):
                # Login bem-sucedido: armazena o ID do usuário na sessão
                session['user_id'] = usuario['id']
                session['user_name'] = usuario['nome']
                flash(f'Bem-vindo(a), {usuario["nome"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Credenciais inválidas. Verifique seu e-mail e senha.', 'danger')
        else:
            flash('Credenciais inválidas. Verifique seu e-mail e senha.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Rota para fazer logout e encerrar a sessão."""
    # Remove o ID do usuário e o nome da sessão
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Você saiu da sua conta com segurança.', 'info')
    return redirect(url_for('index'))

def login_required(f):
    """Decorador para proteger rotas. Garante que haja um 'user_id' na sessão."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rotas da Dashboard e CRUD de Tarefas ---

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """Área restrita onde o usuário pode gerenciar suas tarefas."""
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()
    
    # 1. Cadastro de Nova Tarefa (POST)
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form.get('descricao', '') # A descrição é opcional
        
        if titulo:
            try:
                cursor.execute(
                    "INSERT INTO tarefa (usuario_id, titulo, descricao) VALUES (?, ?, ?)",
                    (user_id, titulo, descricao)
                )
                db.commit()
                flash('Tarefa adicionada com sucesso!', 'success')
            except Exception as e:
                flash(f'Erro ao adicionar tarefa: {e}', 'danger')
        else:
            flash('O título da tarefa é obrigatório.', 'warning')
        
        return redirect(url_for('dashboard'))

    # 2. Listagem de Tarefas (GET)
    cursor.execute("SELECT id, titulo, descricao FROM tarefa WHERE usuario_id = ? ORDER BY id DESC", (user_id,))
    tarefas = cursor.fetchall()
    
    return render_template('dashboard.html', tarefas=tarefas)

@app.route('/excluir_tarefa/<int:tarefa_id>', methods=['POST'])
@login_required
def excluir_tarefa(tarefa_id):
    """Rota para excluir uma tarefa específica."""
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Garante que o usuário só possa excluir SUAS próprias tarefas
        cursor.execute(
            "DELETE FROM tarefa WHERE id = ? AND usuario_id = ?",
            (tarefa_id, user_id)
        )
        db.commit()
        
        if cursor.rowcount > 0:
            flash('Tarefa excluída com sucesso!', 'success')
        else:
            flash('Erro: Tarefa não encontrada ou você não tem permissão para excluí-la.', 'danger')
            
    except Exception as e:
        flash(f'Erro ao excluir tarefa: {e}', 'danger')
        
    return redirect(url_for('dashboard'))

# Inicializa o banco de dados antes da primeira requisição
if __name__ == '__main__':
    # Esta linha garante que as tabelas sejam criadas ao iniciar
    init_db() 
    app.run(debug=True)