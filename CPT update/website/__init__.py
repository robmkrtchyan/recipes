from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'du apush es'

    from .index import index

    app.register_blueprint(index, url_prefix = '/')

    return app