from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from .forms import IdeaGenerationForm, VideoCreationForm
from .models import Favorite
from .utilities.youtube_helpers import get_channel_info
from .utilities.gpt_helpers import generate_ideas_prompt, generate_video_content
from .utilities.video_helpers import create_video_from_elements
from .utilities.image_helpers import generate_images_for_video
from .utilities.audio_helpers import generate_audio_for_script
from .utilities.animations_helpers import animate_images
from .utilities.subtitles_helpers import generate_subtitles_for_video
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def index():
    return render_template('index.html')

@views.route('/channel/connect', methods=['GET', 'POST'])
@login_required
def channel_connect():
    if request.method == 'POST':
        # Here you would have logic to connect to the YouTube API and retrieve channel info
        # For now, we'll simulate with a placeholder function
        channel_info = get_channel_info(current_user)
        if channel_info:
            session['channel_info'] = channel_info
            flash('YouTube channel connected successfully!', 'success')
            return redirect(url_for('views.idea_generation'))
        else:
            flash('Failed to connect YouTube channel.', 'danger')
    return render_template('channel_connect.html')

@views.route('/ideas/generate', methods=['GET', 'POST'])
@login_required
def idea_generation():
    form = IdeaGenerationForm()
    if form.validate_on_submit():
        channel_info = session.get('channel_info', {})
        prompt = generate_ideas_prompt(channel_info['description'], channel_info['name'])
        ideas = generate_video_content(prompt)
        return render_template('idea_generation.html', form=form, ideas=ideas)
    return render_template('idea_generation.html', form=form)

@views.route('/ideas/favorite', methods=['POST'])
@login_required
def favorite_idea():
    idea_id = request.form.get('idea_id')
    if idea_id:
        # Here you would add the idea to the user's favorites
        # For now, we'll simulate with a placeholder
        favorite = Favorite(user_id=current_user.id, idea_id=idea_id)
        db.session.add(favorite)
        db.session.commit()
        flash('Idea added to favorites!', 'success')
    else:
        flash('Invalid idea selected.', 'danger')
    return redirect(url_for('views.idea_generation'))

@views.route('/video/create', methods=['GET', 'POST'])
@login_required
def video_creation():
    form = VideoCreationForm()
    if form.validate_on_submit():
        # Here you would generate the video content using GPT-3
        script, title, description, hashtags = generate_video_content(form.idea.data)
        audio = generate_audio_for_script(script)
        images = generate_images_for_video(script)
        video = create_video_from_elements(images, audio)
        subtitles = generate_subtitles_for_video(script)
        animate_images(video, images)
        # Save the video and related content to the database or file system
        flash('Video created successfully!', 'success')
        return redirect(url_for('views.index'))
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('video_creation.html', form=form, favorites=favorites)