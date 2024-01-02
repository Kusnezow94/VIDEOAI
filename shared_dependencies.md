Shared Dependencies:

- **Flask**: A micro web framework written in Python, used across all Flask-related Python files.
- **Flask-Login**: Provides user session management for Flask, used in `app/__init__.py`, `app/auth_views.py`, `app/decorators.py`.
- **Flask-WTF**: Integrates Flask with WTForms, used in `app/forms.py`.
- **Flask-SQLAlchemy**: Adds SQLAlchemy support to Flask, used in `app/__init__.py`, `app/models.py`.
- **Flask-Migrate**: Handles SQLAlchemy database migrations for Flask applications, used in `app/__init__.py`, `migrations/`.
- **Flask-Mail**: Provides Flask email sending support, used in `app/email.py`, `app/utilities/email_helpers.py`.
- **Flask-Bootstrap**: Integrates Bootstrap with Flask, used in `app/__init__.py`.
- **Flask-Script**: Adds support for writing external scripts in Flask, used in `run.py`.
- **python-dotenv**: Reads key-value pairs from a `.env` file and sets them as environment variables, used in `.env`, `.flaskenv`.
- **WTForms**: A flexible forms validation and rendering library for Python web development, used in `app/forms.py`.
- **SQLAlchemy**: The Python SQL toolkit and Object-Relational Mapper, used in `app/models.py`.
- **OAuthLib**: A generic, spec-compliant, thorough implementation of the OAuth request-signing logic, used in `app/utilities/youtube_helpers.py`.
- **requests**: Allows you to send HTTP/1.1 requests using Python, used in `app/utilities/api_helpers.py`, `app/utilities/youtube_helpers.py`.
- **openai**: The official OpenAI API client library for Python, used in `app/utilities/gpt_helpers.py`.
- **Pillow**: The Python Imaging Library adds image processing capabilities, used in `app/utilities/image_helpers.py`.
- **moviepy**: Video editing library, used in `app/utilities/animations_helpers.py`.
- **itsdangerous**: Various helpers to pass trusted data to untrusted environments and back, used in `app/utilities/security_helpers.py`.

Exported Variables:
- `SECRET_KEY`: Used in `config.py`, `instance/config.py`.
- `SQLALCHEMY_DATABASE_URI`: Used in `config.py`, `instance/config.py`.
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`: Used in `config.py`, `instance/config.py`, `app/email.py`.

Data Schemas:
- `User`: Defined in `app/models.py`, used in `app/auth_views.py`, `app/views.py`.
- `Favorite`: Defined in `app/models.py`, used in `app/views.py`, `app/video_views.py`.

ID Names of DOM Elements:
- `login-form`: Used in `app/templates/login.html`, `app/static/js/main.js`.
- `register-form`: Used in `app/templates/register.html`, `app/static/js/main.js`.
- `forgot-password-form`: Used in `app/templates/forgot_password.html`, `app/static/js/main.js`.
- `reset-password-form`: Used in `app/templates/reset_password.html`, `app/static/js/main.js`.
- `generate-ideas-button`: Used in `app/templates/idea_generation.html`, `app/static/js/main.js`.
- `create-video-button`: Used in `app/templates/video_creation.html`, `app/static/js/main.js`.

Message Names:
- `flash-messages`: Used in `app/templates/base.html`, `app/auth_views.py`, `app/views.py`.

Function Names:
- `login_user`: Used in `app/auth_views.py`, `app/decorators.py`.
- `logout_user`: Used in `app/auth_views.py`, `app/views.py`.
- `generate_password_hash`, `check_password_hash`: Used in `app/models.py`, `app/auth_views.py`.
- `send_email`: Used in `app/email.py`, `app/auth_views.py`.
- `login_required`: Used in `app/decorators.py`, `app/views.py`.
- `youtube_connect`: Used in `app/youtube_views.py`, `app/views.py`.
- `generate_ideas`: Used in `app/gpt3_views.py`, `app/views.py`.
- `create_video`: Used in `app/video_views.py`, `app/views.py`.
- `generate_audio`: Used in `app/utilities/audio_helpers.py`, `app/video_views.py`.
- `generate_images`: Used in `app/utilities/image_helpers.py`, `app/video_views.py`.
- `animate_images`: Used in `app/utilities/animations_helpers.py`, `app/video_views.py`.
- `generate_subtitles`: Used in `app/utilities/subtitles_helpers.py`, `app/video_views.py`.