from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app
from flask_login import login_required, current_user
from app.utilities.api_helpers import make_api_request
from app.utilities.youtube_helpers import get_youtube_service, get_channel_details
from app.models import db, User
from app.forms import ConnectYouTubeForm

youtube_views = Blueprint('youtube_views', __name__, template_folder='templates')

@youtube_views.route('/connect_youtube', methods=['GET', 'POST'])
@login_required
def connect_youtube():
    form = ConnectYouTubeForm()
    if form.validate_on_submit():
        # Assuming the form contains fields to input API Key and OAuth credentials
        api_key = form.api_key.data
        oauth_credentials = form.oauth_credentials.data

        # Store the API Key and OAuth credentials in the user's session or database
        current_user.youtube_api_key = api_key
        current_user.youtube_oauth_credentials = oauth_credentials
        db.session.commit()

        # Redirect to the route that handles YouTube channel connection
        return redirect(url_for('youtube_views.connect_channel'))

    return render_template('connect_youtube.html', form=form)

@youtube_views.route('/connect_channel', methods=['GET'])
@login_required
def connect_channel():
    try:
        # Retrieve the YouTube service using the stored API Key and OAuth credentials
        youtube_service = get_youtube_service(current_user.youtube_api_key, current_user.youtube_oauth_credentials)

        # Get the user's YouTube channel details
        channel_details = get_channel_details(youtube_service)

        # Store channel details in the session or database
        current_user.youtube_channel_name = channel_details['channel_name']
        current_user.youtube_channel_description = channel_details['channel_description']
        db.session.commit()

        # Redirect to the idea generation page
        return redirect(url_for('youtube_views.idea_generation'))

    except Exception as e:
        flash('Failed to connect YouTube channel: {}'.format(e), 'danger')
        return redirect(url_for('main_views.index'))

@youtube_views.route('/idea_generation', methods=['GET'])
@login_required
def idea_generation():
    # Check if the channel details are available
    if not current_user.youtube_channel_name or not current_user.youtube_channel_description:
        flash('You need to connect your YouTube channel first.', 'warning')
        return redirect(url_for('youtube_views.connect_youtube'))

    # Prepare the prompt for GPT-3.5 using the channel details
    prompt = f"Generate three creative video ideas for YouTube Shorts based on the channel: {current_user.youtube_channel_name}, which focuses on: {current_user.youtube_channel_description}"

    # Send the prompt to GPT-3.5 and get the ideas
    try:
        response = make_api_request(prompt, engine='gpt-3.5', max_tokens=150)
        ideas = response.get('choices', [])[0].get('text', '').split('\n')

        # Render the idea generation page with the generated ideas
        return render_template('idea_generation.html', ideas=ideas)

    except Exception as e:
        flash('Failed to generate ideas: {}'.format(e), 'danger')
        return redirect(url_for('main_views.index'))