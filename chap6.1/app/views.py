from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import login_user
from flask.ext.login import logout_user
from app import app
from app import login_manager
from forms import LoginForm


@app.route('/')

def homepage():
    name = request.args.get('name')
    number = request.args.get('number')
    return render_template('homepage.html', name=name, number=number)

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user, remember=form.remember_me.data)
            flash("Successfully logged in as %s." % form.user.email,"success")
            return redirect(request.args.get("next") or url_for("homepage"))
    else:
        form = LoginForm()

    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    logout_user()
    flash('You habe been logged out.', 'success')
    return redirect(request.args.get('next') or url_for('homepage'))
