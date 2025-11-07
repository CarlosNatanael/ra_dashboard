import sqlite3
from flask import Flask, render_template, g, request, redirect, url_for

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print("Banco de dados inicializado.")

@app.cli.command('init-db')
def init_db_command():
    init_db()

@app.route('/add', methods=['POST'])
def add_entry():
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
    return redirect(url_for('index'))

@app.route('/')
def index():
    db = get_db()
    queue_items = db.execute (
        'SELECT id, game_id, developer_username, date_requested, status, reviewer_username'
        ' FROM review_queue'
        ' ORDER BY date_requested ASC'
    ).fetchall()
    return render_template('index.html', queue=queue_items)