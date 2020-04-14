from flask import render_template, redirect, url_for, flash

from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}.", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@email.com" and form.password.data == "password":
            flash(f"Successfully logged in", "success")
            return redirect(url_for("home"))
        else:
            flash(f"Unable to log in. Please check your email and password.", "danger")

    return render_template("login.html", title="Login", form=form)
