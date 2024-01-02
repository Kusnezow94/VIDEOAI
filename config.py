import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    # YouTube API Configurations
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

    # OpenAI API Configurations
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # ElevenLabs API Configurations
    ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')

    # DALL-E API Configurations
    DALL_E_API_KEY = os.environ.get('DALL_E_API_KEY')