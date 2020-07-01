from flask import Flask, render_template
from flask_bootstrap import Bootstrap, WebCDN

from .database import db_session, init_db

from .frontend import frontend
from .nav import nav
from .auth import login_manager

# init_db()

def create_app():
    app = Flask(__name__)
    
    app.config.update(SECRET_KEY="devkey")

    Bootstrap(app)
    app.extensions['bootstrap']['cdns']['bootstrap'] = WebCDN('https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.3.7/')
    app.extensions['bootstrap']['cdns']['jquery'] = WebCDN('https://cdn.bootcdn.net/ajax/libs/jquery/1.12.4/')
    
    nav.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(frontend)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app 


