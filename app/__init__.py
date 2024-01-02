from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the configuration from the instance folder
app.config.from_object(Config)
app.config.from_pyfile('config.py')

# Initialize plugins
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bootstrap = Bootstrap(app)
mail = Mail(app)

# Register blueprints
from app.auth_views import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from app.main_views import main as main_blueprint
app.register_blueprint(main_blueprint)

from app.youtube_views import youtube as youtube_blueprint
app.register_blueprint(youtube_blueprint)

from app.gpt3_views import gpt3 as gpt3_blueprint
app.register_blueprint(gpt3_blueprint)

from app.video_views import video as video_blueprint
app.register_blueprint(video_blueprint)

# Import models to ensure they are known to SQLAlchemy
from app import models

# Ensure the instance folder exists
import os
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Application factory pattern
def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(youtube_blueprint, url_prefix='/youtube')
    app.register_blueprint(gpt3_blueprint, url_prefix='/gpt3')
    app.register_blueprint(video_blueprint, url_prefix='/video')

    with app.app_context():
        db.create_all()

    return app

# Check if the run.py file is executing this script directly and not importing it
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)