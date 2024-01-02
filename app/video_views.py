from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import Favorite
from app.utilities.gpt_helpers import generate_script
from app.utilities.audio_helpers import generate_audio
from app.utilities.image_helpers import generate_images
from app.utilities.animations_helpers import animate_images
from app.utilities.subtitles_helpers import generate_subtitles
from app.utilities.video_helpers import compile_video
from app import db

video_views = Blueprint('video_views', __name__)

@video_views.route('/video_creation', methods=['GET', 'POST'])
@login_required
def video_creation():
    if request.method == 'POST':
        # Retrieve the selected favorite idea
        favorite_id = request.form.get('favorite_id')
        favorite = Favorite.query.get(favorite_id)
        if not favorite or favorite.user_id != current_user.id:
            flash('Video idea not found or access denied.', 'danger')
            return redirect(url_for('main_views.index'))

        # Generate script, title, description, and hashtags with GPT-3
        script_data = generate_script(favorite.idea)
        if not script_data:
            flash('Failed to generate video script.', 'danger')
            return redirect(url_for('main_views.index'))

        # Generate audio with ElevenLabs
        audio_file = generate_audio(script_data['script'])
        if not audio_file:
            flash('Failed to generate audio.', 'danger')
            return redirect(url_for('main_views.index'))

        # Generate images with DALL-E every 6 seconds
        image_files = generate_images(script_data['script'])
        if not image_files:
            flash('Failed to generate images.', 'danger')
            return redirect(url_for('main_views.index'))

        # Animate images and create a full video
        video_file = animate_images(image_files, audio_file)
        if not video_file:
            flash('Failed to animate images.', 'danger')
            return redirect(url_for('main_views.index'))

        # Generate subtitles for the video
        subtitles_file = generate_subtitles(script_data['script'])
        if not subtitles_file:
            flash('Failed to generate subtitles.', 'danger')
            return redirect(url_for('main_views.index'))

        # Compile the final video with all generated data
        final_video_file = compile_video(video_file, subtitles_file)
        if not final_video_file:
            flash('Failed to compile the final video.', 'danger')
            return redirect(url_for('main_views.index'))

        # Save the video file path to the favorite for later use
        favorite.video_file_path = final_video_file
        db.session.commit()

        flash('Video created successfully!', 'success')
        return redirect(url_for('main_views.index'))

    # Display the user's favorite ideas
    favorites = current_user.favorites.all()
    return render_template('video_creation.html', favorites=favorites)