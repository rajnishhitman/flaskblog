import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message

from flaskblog import app, mail
from flaskblog.globals import default_image


def save_picture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = f"{secrets.token_hex(8)}{f_ext}"
    picture_path = os.path.join(app.root_path, "static", "profile_pics", picture_name)
    # Resize image before saving it
    output_image = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_image)
    image.save(picture_path)
    return picture_name

def delete_picture(picture_name):
    filepath = os.path.join(app.root_path, "static", "profile_pics", picture_name)
    if picture_name != default_image and os.path.isfile(filepath):
        os.remove(filepath)
        print(f"{filepath} removed from profile pics")

def send_reset_email(user):
    print(f"Email sent to {user.username} at {user.email}")
    token = user.get_reset_token()
    print(f"token: {token}")
    msg = Message("Request to Reset Password", recipients=[user.email])
    msg.sender = ("Flaskblog Team", "no-reply@flaskblog.io")
    msg.html = f"""<body style="font-family: sans-serif; font-size: 16px; line-height: 24px;">
<h1 style="font-size: 24px; line-height: 32px;">Hello {user.username}!</h1>
<p>
    It looks like you've requested to reset your Flaskblog's password. If that really is the case, you only need to follow the link <a href="{url_for("users.reset_token", token=token, _external=True)}">Reset Password</a>.
</p>
<p>
Otherwise, you can just ignore this email and nothing will be changed.
</p>
<p>
Thanks for being a valuable member! Happy Bloging!
</p>
<p>
The Flaskblog Team
<span style="font-size: 24px; color: red;">&hearts;</span>
<span style="font-size: 24px; color: green;">&hearts;</span>
<span style="font-size: 24px; color: blue;">&hearts;</span>
</p>
</body>
    """
    mail.send(msg)
