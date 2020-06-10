from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from .database import db_session

from .frontend import frontend
from .nav import nav

def create_app():
    app = Flask(__name__)
    
    app.config.update(SECRET_KEY="devkey")

    Bootstrap(app)

    app.register_blueprint(frontend)
    nav.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app 


