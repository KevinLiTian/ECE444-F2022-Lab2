from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from forms import NameForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "dfjowiefhodsanfd"

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()

    if form.validate_on_submit():

        old_name = session.get("name")
        old_email = session.get("email")
        new_name = form.name.data
        new_email = form.email.data

        if old_name is not None and old_name != new_name:
            flash("Looks like you have changed your name!")
        if old_email is not None and old_email != new_email:
            flash("Looks like you have changed your email!")

        session["name"] = new_name
        session["email"] = new_email

        if "utoronto" in new_email:
            session["message"] = f"Your UofT email is {new_email}"
        else:
            session["message"] = "Please use your UofT email."

        return redirect(url_for("index"))

    return render_template(
        "index.html",
        name=session.get("name"),
        form=form,
        message=session.get("message"),
    )


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
