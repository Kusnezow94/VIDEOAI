from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app.models import User, Favorite
from app.forms import IdeaGenerationForm
from app.utilities.gpt_helpers import generate_ideas
from app.utilities.youtube_helpers import get_channel_info

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/channel_connect', methods=['GET', 'POST'])
@login_required
def channel_connect():
    if 'youtube_access_token' not in session:
        return redirect(url_for('youtube_views.authorize'))

    channel_info = get_channel_info(session['youtube_access_token'])
    if channel_info:
        session['channel_description'] = channel_info['description']
        session['channel_name'] = channel_info['title']
        flash('YouTube channel connected successfully!', 'success')
    else:
        flash('Failed to connect YouTube channel. Please try again.', 'danger')

    return render_template('channel_connect.html', channel_name=session.get('channel_name'))

@main.route('/idea_generation', methods=['GET', 'POST'])
@login_required
def idea_generation():
    form = IdeaGenerationForm()
    if form.validate_on_submit():
        description = session.get('channel_description', '')
        name = session.get('channel_name', '')
        prompt = f"Generate video ideas for YouTube Shorts based on the channel: {name} with description: {description}"
        ideas = generate_ideas(prompt)
        session['generated_ideas'] = ideas
        return render_template('idea_generation.html', ideas=ideas, form=form)
    return render_template('idea_generation.html', form=form)

@main.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorites():
    if 'favorite_ideas' not in session:
        session['favorite_ideas'] = []

    if 'selected_idea' in session:
        if session['selected_idea'] not in session['favorite_ideas']:
            session['favorite_ideas'].append(session['selected_idea'])
            flash('Idea added to favorites!', 'success')
        else:
            flash('Idea is already in favorites.', 'info')
        session.pop('selected_idea', None)

    return render_template('favorites.html', favorite_ideas=session['favorite_ideas'])

@main.route('/add_to_favorites/<int:idea_id>', methods=['POST'])
@login_required
def add_to_favorites(idea_id):
    generated_ideas = session.get('generated_ideas', [])
    if idea_id < len(generated_ideas):
        session['selected_idea'] = generated_ideas[idea_id]
        return redirect(url_for('main.favorites'))
    else:
        flash('Invalid idea selected.', 'danger')
        return redirect(url_for('main.idea_generation'))

@main.route('/video_creation', methods=['GET', 'POST'])
@login_required
def video_creation():
    favorite_ideas = session.get('favorite_ideas', [])
    return render_template('video_creation.html', favorite_ideas=favorite_ideas)

@main.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth_views.logout'))