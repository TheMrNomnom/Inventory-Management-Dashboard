# Create a inventory tracking system in Flask using SQL.

from flask import Flask, render_template, request, redirect, flash, jsonify, session
from cs50 import SQL
from tempfile import mkdtemp
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from flask_sqlalchemy import SQLAlchemy

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Auto-reload templates when changes are made
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# TODO convert CS50 SQL to SQLite
db = SQL("sqlite:///inventory.db")


@app.route("/")
@login_required
def index():
    """Homepage that displays all items in inventory, their quantity, and their location."""
    items = db.execute("SELECT * FROM inventory ORDER BY location_id")
    locations = db.execute("SELECT * FROM locations")
    for _ in range(len(items)):
        for location in locations:
            if items[_]["location_id"] == location["id"]:
                items[_]["location_name"] = location["location_name"]
    return render_template("index.html", items=items)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     session.clear()

#     if request.method == "POST":

#         if not request.form.get("username"):
#             flash("Must provide username")
#             return redirect("/login")

#         elif not request.form.get("password"):
#             flash("Must provide password")
#             return redirect("/login")

#         rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#             flash("Invalid username and/or password")
#             return redirect("/login")

#         session["user_id"] = rows[0]["id"]

#         return redirect("/")

#     else:
#         return render_template("login.html")


# @app.route("/logout")
# def logout():
#     """Log user out"""

#     session.clear()

#     return redirect("/")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     """Register user"""

#     if request.method == "POST":
#         print(request.form.get("username"))
#         print(request.form.get("password"))
#         if not request.form.get("username"):
#             flash("Must provide username")
#             return redirect("/register")

#         elif not request.form.get("password"):
#             flash("Must provide password")
#             return redirect("/register")

#         elif not request.form.get("confirmation"):
#             flash("Must reenter password for confirmation")
#             return redirect("/register")

#         elif request.form.get("password") != request.form.get("confirmation"):
#             flash("Passwords do not match")
#             return redirect("/register")

#         rows = db.execute("SELECT * FROM users WHERE username = ?",
#                           request.form.get("username"))

#         if len(rows) > 0:
#             flash("Username already exists")
#             return redirect("/register")

#         lowercase = 0
#         uppercase = 0
#         special = 0
#         digits = 0

#         p = request.form.get("password")

#         if len(p) >= 8:
#             for i in p:

#                 if (i.islower()):
#                     lowercase += 1

#                 if (i.isupper()):
#                     uppercase += 1

#                 if (i.isdigit()):
#                     digits += 1

#                 if(i == '@' or i == '$' or i == '_'):
#                     special += 1

#         if (lowercase < 1 and uppercase < 1 and special < 1 and digits < 1 and lowercase + uppercase + digits + special != len(p)):
#             flash("Password does not match complexity requirements")
#             return redirect("/register")

#         password_hash = generate_password_hash(request.form.get("password"))

#         db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
#                    request.form.get("username"), password_hash)
#         db.commit()
#         return redirect("/login")

#     return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
# @login_required
def add():
    """Add inventory or locations to database"""
    if request.method == "POST":
        if request.form["submitButton"] == "add_item":
            item_name = request.form.get("item_name")
            quantity = request.form.get("quantity")
            location_id = request.form.get("location_list")
            if not item_name or not quantity or location_id == "Location":
                flash("Please fill out all fields")
                return redirect("/add")
            if quantity.isnumeric() == False or int(quantity) < 1:
                flash("Please enter a valid quantity")
                return redirect("/add")
            db.execute("INSERT INTO inventory (item_name, quantity, location_id) VALUES (:item_name, :quantity, :location_id)",
                       item_name=item_name, quantity=quantity, location_id=location_id)
            db.commit()
            return redirect("/")
        elif request.form["submitButton"] == "add_location":
            location_name = request.form.get("location_name")
            if not location_name:
                flash("Please fill out all fields")
                return redirect("/add")
            db.execute("INSERT INTO locations (location_name) VALUES (:location_name)",
                       location_name=location_name)
            db.commit()
            return redirect("/")
    else:
        locations = db.execute("SELECT * FROM locations")
        return render_template("add.html", locations=locations)


@app.route("/delete", methods=["GET", "POST"])
# @login_required
def delete():
    """Delete inventory from database"""
    if request.method == "POST":
        if request.form["submitButton"] == "delete_item":
            item_id = request.form.get("delete_list")
            if item_id == "Item":
                flash("Please select an item to delete")
                return redirect("/delete")
            db.execute("DELETE FROM inventory WHERE id = :item_id",
                       item_id=item_id)
            db.commit()
            return redirect("/")
        elif request.form["submitButton"] == "delete_location":
            location_id = request.form.get("delete_location_list")
            reassign = request.form.get("reassign")
            reassigned_location_id = request.form.get("reassign_location_list")
            if location_id == "Location":
                flash("Please select a location to delete")
                return redirect("/delete")
            if reassign == "off" and reassigned_location_id != "(Only for reassignment) Location":
                flash(
                    "Please check off the reassignment checkbox before selecting a new location")
                return redirect("/delete")
            if reassign == "on" and reassigned_location_id == "(Only for reassignment) Location":
                flash("Please select a location to reassign items to")
                return redirect("/delete")
            if reassign == "on":
                db.execute("UPDATE inventory SET location_id = :reassigned_location_id WHERE location_id = :location_id",
                           reassigned_location_id=reassigned_location_id, location_id=location_id)
                db.execute(
                    "DELETE FROM locations WHERE id = :location_id", location_id=location_id)
                db.commit()
                return redirect("/")

            db.execute(
                "DELETE FROM inventory WHERE location_id = :location_id", location_id=location_id)
            db.execute("DELETE FROM locations WHERE id = :location_id",
                       location_id=location_id)
            db.commit()
            return redirect("/")
    else:
        items = db.execute("SELECT * FROM inventory")
        locations = db.execute("SELECT * FROM locations")
        return render_template("delete.html", items=items, locations=locations)


@app.route("/edit", methods=["GET", "POST"])
# @login_required
def edit():
    """Edit inventory entries"""
    if request.method == "POST":
        if request.form["submitButton"] == "edit_item":
            item_id = request.form.get("item_list")
            quantity = request.form.get("quantity")
            location_id = request.form.get("location_list")
            if item_id == "Item" or not quantity or location_id == "Location":
                flash("Please fill out all fields")
                return redirect("/edit")
            if quantity.isnumeric() == False or int(quantity) < 1:
                flash("Please enter a valid quantity")
                return redirect("/edit")
            db.execute("UPDATE inventory SET quantity = :quantity, location_id = :location_id WHERE id = :item_id",
                       item_id=item_id, quantity=quantity, location_id=location_id)
            db.commit()
            return redirect("/")
        elif request.form["submitButton"] == "edit_location":
            location_id = request.form.get("location_list_second")
            print(location_id)
            location_name = request.form.get("new_location_name")
            print(location_name)
            if location_id == "Location" or not location_name:
                flash("Please fill out all fields")
                return redirect("/edit")
            db.execute("UPDATE locations SET location_name = :location_name WHERE id = :location_id",
                       location_id=location_id, location_name=location_name)
            db.commit()
            return redirect("/")
    else:
        items = db.execute("SELECT * FROM inventory")
        locations = db.execute("SELECT * FROM locations")
        return render_template("edit.html", items=items, locations=locations)


@app.route("/item_info")
# @login_required
def item_info():
    """Return all item info"""
    item_id = request.args.get("item_id")
    item = db.execute(
        "SELECT * FROM inventory WHERE id = :item_id", item_id=item_id)
    return jsonify(item)


@app.route("/location_info")
# @login_required
def location_info():
    """Return location of item"""
    item_id = request.args.get("item_id")
    location = db.execute(
        "SELECT * FROM locations JOIN inventory ON locations.id = inventory.location_id WHERE inventory.id = :item_id", item_id=item_id)
    return jsonify(location)
