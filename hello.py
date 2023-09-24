from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap

from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = EmailField("What is your UofT Email address?", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")
        old_email = session.get("email")
        if old_email is not None and old_email != form.email.data:
            flash("Looks like you have changed your email!")
        
        session["name"] = form.name.data
        invalid_email = "utoronto" not in form.email.data
        session["invalid_email"] = invalid_email
        session["email"] = "invalid" if invalid_email else form.email.data
        return redirect(url_for("index"))
    return render_template("index.html", form=form, name=session.get("name"), invalid_email=session.get("invalid_email"), email=session.get("email"))

@app.route("/user/<name>")
def user(name):
    return render_template(
        "user.html",
        name=name,
        current_time=datetime.utcnow()
    )

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run()
