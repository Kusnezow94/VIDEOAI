from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import login_required, current_user
from app.utilities.gpt_helpers import generate_prompt, call_openai_api
from app.models import Favorite, db
from app.forms import IdeaForm

gpt3_blueprint = Blueprint('gpt3', __name__)

@gpt3_blueprint.route('/generate_ideas', methods=['GET', 'POST'])
@login_required
def generate_ideas():
    form = IdeaForm()
    if form.validate_on_submit():
        channel_description = session.get('channel_description', '')
        channel_name = session.get('channel_name', '')
        prompt = generate_prompt(channel_description, channel_name)
        ideas = call_openai_api(prompt)
        
        if ideas:
            session['generated_ideas'] = ideas
            return render_template('idea_generation.html', ideas=ideas, form=form)
        else:
            flash('Failed to generate ideas. Please try again.', 'danger')
            return redirect(url_for('main.index'))
    
    return render_template('idea_generation.html', form=form)

@gpt3_blueprint.route('/favorite_idea/<int:idea_id>', methods=['POST'])
@login_required
def favorite_idea(idea_id):
    ideas = session.get('generated_ideas', [])
    if ideas and 0 <= idea_id < len(ideas):
        idea = ideas[idea_id]
        new_favorite = Favorite(user_id=current_user.id, idea=idea)
        db.session.add(new_favorite)
        db.session.commit()
        flash('Idea added to favorites!', 'success')
    else:
        flash('Invalid idea selected.', 'danger')
    
    return redirect(url_for('gpt3.generate_ideas'))