from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# Usuarios válidos
users = {
    "admin": "password123"  # Cambia esto a un usuario y contraseña seguros
}
app.config['DATABASE'] = 'instance/posts.sqlite'

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
        db.commit()

# Datos iniciales
custom_query_result = [
    {"title": "Título de la Publicación 1", "excerpt": "Extracto de la publicación 1"},
    {"title": "Título de la Publicación 2", "excerpt": "Extracto de la publicación 2"},
    {"title": "Título de la Publicación 3", "excerpt": "Extracto de la publicación 3"},
    {"title": "Título de la Publicación 4", "excerpt": "Extracto de la publicación 4"}
]

# Decorador para requerir inicio de sesión
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Por favor, inicia sesión primero.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Has iniciado sesión exitosamente.', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        title = request.form['title']
        address = request.form['address']
        excerpt = request.form['excerpt']
        
        db = get_db()
        db.execute('INSERT INTO posts (title, address, excerpt) VALUES (?, ?, ?)',
                   (title, address, excerpt))
        db.commit()
        return redirect(url_for('admin'))
    
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('admin.html', posts=posts)

@app.route('/')
def index():

    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('index.html', posts=posts)


@app.route('/picadas')
def detail():
    # Simulando el query personalizado para obtener publicaciones de la categoría "picadas"
    custom_query_result = [
        {"title": "Título de la Publicación 1", "excerpt": "Extracto de la publicación 1"},
        {"title": "Título de la Publicación 2", "excerpt": "Extracto de la publicación 2"},
        {"title": "Título de la Publicación 3", "excerpt": "Extracto de la publicación 3"},
        {"title": "Título de la Publicación 4", "excerpt": "Extracto de la publicación 4"}
    ]
    return render_template('lugar_detail.html', posts=custom_query_result)



@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        address = request.form['address']
        excerpt = request.form['excerpt']
        
        db.execute('UPDATE posts SET title = ?, address = ?, excerpt = ? WHERE id = ?',
                   (title, address, excerpt, id))
        db.commit()
        return redirect(url_for('admin'))
    
    return render_template('edit_post.html', post=post)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
