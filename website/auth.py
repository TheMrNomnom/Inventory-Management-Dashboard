from flask import Blueprint, url_for, redirect, render_template, request, flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if request.method == "POST":

        if not request.form.get("username"):
            flash("Must provide username")
            return redirect(url_for("auth.login"))

        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(username=request.form.get("username")).first()

        if user:
            if check_password_hash(user.hash, request.form.get("password")):
                flash("Logged in")
                login_user(user, remember=True)
                return redirect(url_for("views.index"))
            else:
                flash("Incorrect password")
                return redirect(url_for("auth.login"))
        else:
            flash("Username is invalid")
            return redirect(url_for("auth.login"))

    else:
        return render_template("login.html", user = current_user)

@auth.route("/logout")
@login_required
def logout():
    """Log user out"""

    logout_user()

    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        if not request.form.get("username"):
            flash("Must provide username")
            return redirect(url_for("auth.register"))

        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect(url_for("auth.register"))

        elif not request.form.get("confirmation"):
            flash("Must reenter password for confirmation")
            return redirect(url_for("auth.register"))

        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match")
            return redirect(url_for("auth.register"))

        elif User.query.filter_by(username=request.form.get("username")).first():
            flash("Username already exists")
            return redirect(url_for("auth.register"))

        elif len(request.form.get("username")) > 20:
            flash("Username must be less than 20 characters")
            return redirect(url_for("auth.register"))

        lowercase = 0
        uppercase = 0
        special = 0
        digits = 0

        p = request.form.get("password")

        if len(p) >= 8:
            for i in p:

                if (i.islower()):
                    lowercase += 1

                if (i.isupper()):
                    uppercase += 1

                if (i.isdigit()):
                    digits += 1

                if(i == '@' or i == '$' or i == '_'):
                    special += 1

        if (lowercase < 1 and uppercase < 1 and special < 1 and digits < 1 and lowercase + uppercase + digits + special != len(p)):
            flash("Password does not match complexity requirements")
            return redirect(url_for("auth.register"))

        password_hash = generate_password_hash(request.form.get("password"))

        new_user = User(request.form.get("username"), password_hash)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html", user = current_user)