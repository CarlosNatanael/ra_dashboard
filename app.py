import sqlite3
from flask import Flask, render_template, g

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    """Conecta ao banco de dados."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
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

@app.route('/')
def index():
    return render_template('index.html')