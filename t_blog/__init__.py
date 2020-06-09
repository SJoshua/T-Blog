from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from .frontend import frontend
from .nav import nav

def create_app():
    app = Flask(__name__)
    
    app.config.update(SECRET_KEY="devkey")

    Bootstrap(app)

    app.register_blueprint(frontend)
    nav.init_app(app)

    return app 