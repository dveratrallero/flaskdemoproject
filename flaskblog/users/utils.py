import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    f_n, f_ext = os.path.splitext(form_picture.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body=f'''To reset your password, please visit the following link:
{url_for('users.reset token', token=token, _external=True)}

If you did not make this request simply ignore this email and no changes will be made.
'''
    mail.send(msg)
