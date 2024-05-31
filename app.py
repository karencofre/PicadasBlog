from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # Simulando el query personalizado para obtener publicaciones de la categoría "picadas"
    custom_query_result = [
        {"title": "Título de la Publicación 1", "excerpt": "Extracto de la publicación 1"},
        {"title": "Título de la Publicación 2", "excerpt": "Extracto de la publicación 2"},
        {"title": "Título de la Publicación 3", "excerpt": "Extracto de la publicación 3"},
        {"title": "Título de la Publicación 4", "excerpt": "Extracto de la publicación 4"}
    ]
    return render_template('index.html', posts=custom_query_result)
if __name__ == '__main__':
    app.run(debug=True)
