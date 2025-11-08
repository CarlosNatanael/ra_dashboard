import sqlite3
from flask import (
    Flask, render_template, g, request, redirect, url_for, session, flash,
)
import functools
import requests

app = Flask(__name__)
DATABASE = 'database.db'
app.config['SECRET_KEY'] = 'Oy6GOQ5nOO3l8H3TkvFMw2QABo7Kw1Mn'

RA_API_URL = "https://retroachievements.org/API"

# --- Gerenciamento do Banco de Dados ---

def get_db():
    """Conecta ao banco de dados."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row 
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Fecha a conexão ao final da requisição."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Lê o arquivo schema.sql e cria o banco de dados."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print("Banco de dados inicializado.")

@app.cli.command('init-db')
def init_db_command():
    init_db()

# --- Gerenciamento de login e autenticação ---

AUTHORIZED_ADMINS = [
    'srleo12'
]

# --- Gerenciamento de Login e Autenticação (Corrigido) ---

def login_required(view):
    """Um 'decorador' que protege as páginas de admin."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('username') is None:
            flash('Você precisa estar logado para ver esta página.', 'error')
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('Você não tem permissão para acessar esta página.', 'error')
            return redirect(url_for('index'))
        return view(**kwargs)
    return wrapped_view

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login."""
    if request.method == 'POST':
        username = request.form['username']
        web_api_key = request.form['web_api_key']
        
        auth_params = { 'z': username, 'y': web_api_key }
        
        try:
            url_to_call = f"{RA_API_URL}/API_GetUserSummary.php?z={username}&y={web_api_key}&u={username}&g=5&a=5"
            response = requests.get(url_to_call)
            response.raise_for_status() 
            data = response.json()
            user_role = int(data.get('Role', 0))
            is_admin = False
            if user_role >= 5:
                is_admin = True
            if data['User'].lower() in AUTHORIZED_ADMINS:
                is_admin = True
            if not is_admin:
                flash(f'Falha no login. Apenas Code Reviewers ou Admins autorizados podem logar.', 'error')
                return render_template('login.html')
            session.clear()
            session['username'] = data['User']
            session['is_admin'] = True
            
            flash(f'Login bem-sucedido! Bem-vindo, {data["User"]}.', 'success')
            return redirect(url_for('admin_panel'))
            
        except requests.exceptions.RequestException as e:
            flash(f'Falha no login. Verifique seu Username e API Key. (Erro: {e})', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Limpa a sessão e desloga o usuário."""
    session.clear()
    flash('Você foi deslogado.', 'success')
    return redirect(url_for('index'))

# --- Rotas do Site Público (Jr. Dev View) ---

@app.route('/')
def index():
    """Página inicial que mostra a fila."""
    db = get_db()
    queue_items = db.execute(
        'SELECT * FROM review_queue ORDER BY date_requested ASC'
    ).fetchall()
    return render_template('index.html', queue=queue_items)


# --- ROTAS DO PAINEL DE ADMIN (Revisor View) ---

@app.route('/admin')
@login_required
def admin_panel():
    db = get_db()
    queue_items = db.execute(
        'SELECT * FROM review_queue ORDER BY date_requested ASC'
    ).fetchall()
    return render_template('admin.html', queue=queue_items)

@app.route('/admin/add', methods=['POST'])
@login_required 
def admin_add():
    game_id = request.form['game_id']
    game_name = request.form['game_name']
    developer_username = request.form['developer_username']
    
    db = get_db()
    db.execute(
        'INSERT INTO review_queue (game_id, game_name, developer_username)'
        ' VALUES (?, ?, ?)',
        (game_id, game_name, developer_username)
    )
    db.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/update/<int:entry_id>', methods=['POST'])
@login_required 
def admin_update(entry_id):
    status = request.form['status']
    reviewer = request.form['reviewer_username']
    
    db = get_db()
    db.execute(
        'UPDATE review_queue SET status = ?, reviewer_username = ?'
        ' WHERE id = ?',
        (status, reviewer, entry_id)
    )
    db.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete/<int:entry_id>')
@login_required 
def admin_delete(entry_id):
    db = get_db()
    db.execute('DELETE FROM review_queue WHERE id = ?', (entry_id,))
    db.commit()
    return redirect(url_for('admin_panel'))