from flask_mail import Message
from flask import current_app
from app import mail

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[YourAppName] Reset Your Password',
               sender=current_app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=f'''To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
''',
               html_body=f'''<p>To reset your password, visit the following link:</p>
<p><a href="{url_for('auth.reset_password', token=token, _external=True)}">Reset Password</a></p>
<p>If you did not make this request then simply ignore this email and no changes will be made.</p>
''')