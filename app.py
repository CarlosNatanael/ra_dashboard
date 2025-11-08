import sqlite3
import functools
import requests
import datetime
from flask import (
    Flask, render_template, g, request, redirect, url_for, session, flash, jsonify
)
from flask_babel import Babel

app = Flask(__name__)
DATABASE = 'database.db'
app.config['SECRET_KEY'] = 'Oy6GOQ5nOO3l8H3TkvFMw2QABo7Kw1Mn'
RA_API_URL = "https://retroachievements.org/API"

# --- CONFIGURAÇÃO DO BABEL ---
app.config['LANGUAGES'] = ['en', 'pt_BR', 'es']
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)

@app.localeselector 
def get_locale():
    """Detecta o idioma do usuário."""
    if 'lang' in session and session['lang'] in app.config['LANGUAGES']:
        return session['lang']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

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

# --- Gerenciamento de Login e Autenticação ---

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
            session['web_api_key'] = web_api_key
            
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

@app.route('/set_lang/<lang>')
def set_lang(lang):
    """Salva a escolha de idioma do usuário na sessão."""
    if lang in app.config['LANGUAGES']:
        session['lang'] = lang 
    referrer = request.referrer
    if referrer:
        return redirect(referrer)
    return redirect(url_for('index'))

# --- API INTERNA ---

@app.route('/api/get-game-name/<int:game_id>')
@login_required
def api_get_game_name(game_id):
    """Pega o nome de um jogo da API do RA usando o ID."""
    try:
        username = session['username']
        web_api_key = session['web_api_key']

        url = f"{RA_API_URL}/API_GetGame.php?z={username}&y={web_api_key}&i={game_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'Title' in data:
            return jsonify({'game_name': data['Title']})
        else:
            return jsonify({'error': 'Game not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    """Mostra o histórico de sets Aprovados."""
    db = get_db()
    queue_items = db.execute(
        "SELECT * FROM review_queue WHERE status = 'Approved' ORDER BY date_requested DESC"
    ).fetchall()
    
    return render_template('history.html', queue=queue_items)

@app.route('/status')
def status_page():
    """Mostra a página estática que explica os status."""
    return render_template('status.html')

@app.route('/api/update-queue')
def api_update_queue():
    """Retorna APENAS o HTML do corpo da tabela da fila."""

    search_term = request.args.get('search', '')
    my_sets_filter = request.args.get('my_sets', '')
    
    db = get_db()

    query = "SELECT * FROM review_queue WHERE status != 'Approved'"
    params = []
    
    if search_term:
        query += " AND (game_name LIKE ? OR developer_username LIKE ?)"
        params.extend([f"%{search_term}%", f"%{search_term}%"])
        
    if my_sets_filter:
        query += " AND developer_username = ?"
        params.append(my_sets_filter)
        
    query += " ORDER BY date_requested ASC"
    
    queue_items = db.execute(query, params).fetchall()
    
    return render_template('_queue_table.html', queue=queue_items)

# --- Rotas do Site Público ---

@app.route('/')
def index():
    """Página inicial que mostra a fila (APENAS sets PENDENTES)."""
    search_term = request.args.get('search', '')
    my_sets_filter = request.args.get('my_sets', '')
    
    db = get_db()
    
    query = "SELECT * FROM review_queue WHERE status != 'Approved'"
    params = []
    
    if search_term:
        query += " AND (game_name LIKE ? OR developer_username LIKE ?)"
        params.extend([f"%{search_term}%", f"%{search_term}%"])
        
    if my_sets_filter:
        query += " AND developer_username = ?"
        params.append(my_sets_filter)
    query += " ORDER BY date_requested ASC"
    queue_items = db.execute(query, params).fetchall()
    
    return render_template(
        'index.html', 
        queue=queue_items, 
        search_term=search_term, 
        my_sets_filter=my_sets_filter
    )

# --- ROTAS DO PAINEL DE ADMIN (Revisor View) ---

@app.route('/admin')
@login_required
def admin_panel():
    db = get_db()
    queue_items = db.execute(
        "SELECT * FROM review_queue WHERE status != 'Approved' ORDER BY date_requested ASC"
    ).fetchall()
    return render_template('admin.html', queue=queue_items)

@app.route('/admin/add', methods=['POST'])
@login_required 
def admin_add():
    """(Admin) Adiciona um novo pedido à fila."""
    game_id = request.form['game_id']
    game_name = request.form['game_name']
    developer_username = request.form['developer_username']
    now_formatted = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    db = get_db()
    db.execute(
        'INSERT INTO review_queue (game_id, game_name, developer_username, date_requested, date_last_updated)'
        ' VALUES (?, ?, ?, ?, ?)',
        (game_id, game_name, developer_username, now_formatted, now_formatted)
    )
    db.commit()
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/update/<int:entry_id>', methods=['POST'])
@login_required 
def admin_update(entry_id):
    """(Admin) Atualiza o status e (opcionalmente) o revisor."""
    
    status = request.form['status']
    action = request.form['action']
    now_formatted = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    db = get_db()
    query_params = {
        'status': status,
        'last_updated': now_formatted,
        'id': entry_id
    }
    if status == 'Approved':
        query_params['date_approved'] = now_formatted
    else:
        query_params['date_approved'] = None 

    if action == 'claim_set':
        query_params['reviewer'] = session['username']
        db.execute(
            'UPDATE review_queue'
            ' SET status = :status, reviewer_username = :reviewer, date_last_updated = :last_updated, date_approved = :date_approved'
            ' WHERE id = :id',
            query_params
        )
    elif action == 'update_status':
        db.execute(
            'UPDATE review_queue'
            ' SET status = :status, date_last_updated = :last_updated, date_approved = :date_approved'
            ' WHERE id = :id',
            query_params
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