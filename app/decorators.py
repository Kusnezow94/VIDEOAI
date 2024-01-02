from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You need to be logged in to view this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def youtube_connected_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_youtube_connected:
            flash('You need to connect your YouTube account to access this feature.', 'warning')
            return redirect(url_for('main.channel_connect'))
        return f(*args, **kwargs)
    return decorated_function

def idea_generation_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.has_generated_ideas:
            flash('You need to generate ideas before accessing this page.', 'info')
            return redirect(url_for('youtube.generate_ideas'))
        return f(*args, **kwargs)
    return decorated_function

def favorite_ideas_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.has_favorite_ideas:
            flash('You need to have favorite ideas to create a video.', 'info')
            return redirect(url_for('main.favorites'))
        return f(*args, **kwargs)
    return decorated_function
