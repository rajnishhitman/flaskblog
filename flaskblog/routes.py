import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from flaskblog import app, bcrypt, db
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User
from flaskblog.globals import default_image

posts = [
    {
        "author": "Marcus Reaiche",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "April 12, 2020"
    },
    {
        "author": "John Doe",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "April 12, 2020"
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pass
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Successfully logged in", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Unable to log in. Please check your email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


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

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # Check if picture was uploaded
        if form.file.data:
            # Save picture locally
            picture_name = save_picture(form.file.data)
            previous_image = current_user.image_file
            current_user.image_file = picture_name
            # Delete previous picture
            delete_picture(previous_image)
        # Update database and redirect to account
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect("account")
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename=f"profile_pics/{current_user.image_file}")
    return render_template("account.html", title="Account", image_file=image_file, form=form)
