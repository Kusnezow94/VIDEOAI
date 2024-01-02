from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bootstrap = Bootstrap(app)
mail = Mail(app)

# Register blueprints
from app.auth_views import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from app.main_views import main as main_blueprint
app.register_blueprint(main_blueprint)

from app.youtube_views import youtube as youtube_blueprint
app.register_blueprint(youtube_blueprint, url_prefix='/youtube')

from app.gpt3_views import gpt3 as gpt3_blueprint
app.register_blueprint(gpt3_blueprint, url_prefix='/gpt3')

from app.video_views import video as video_blueprint
app.register_blueprint(video_blueprint, url_prefix='/video')

# Import models to ensure they are known to SQLAlchemy
from app import models

# Check for environment variables for production
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])