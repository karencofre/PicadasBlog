from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# Usuarios válidos
users = {
    "admin": "password123"  # Cambia esto a un usuario y contraseña seguros
}

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
        excerpt = request.form['excerpt']
        custom_query_result.append({"title": title, "excerpt": excerpt})
        return redirect(url_for('admin'))
    
    return render_template('admin.html', custom_query_result=custom_query_result)


@app.route('/')
def index():
    # Simulando el query personalizado para obtener todas las publicaciones
    custom_query_result = [
        {"title": "Título de la Publicación 1", "excerpt": "Extracto de la publicación 1"},
        {"title": "Título de la Publicación 2", "excerpt": "Extracto de la publicación 2"},
        {"title": "Título de la Publicación 3", "excerpt": "Extracto de la publicación 3"},
        {"title": "Título de la Publicación 4", "excerpt": "Extracto de la publicación 4"}
    ]
    return render_template('index.html', posts=custom_query_result)


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


if __name__ == '__main__':
    app.run(debug=True)
