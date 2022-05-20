from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from . import db
from .models import Item, Location
from .helpers import query_to_dict

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def index():
    """Homepage that displays all items in inventory, their quantity, and their location."""
    items = Item.query.all()
    items = query_to_dict(items)
    locations = Location.query.all()
    locations = query_to_dict(locations)

    # Associate location name with item
    for _ in range(len(items)):
        for location in locations:
            if items[_]["location_id"] == location["id"]:
                items[_]["location_name"] = location["name"]

    return render_template("index.html", items=items, user=current_user)


@views.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add inventory or locations to database"""
    if request.method == "POST":

        if request.form["submitButton"] == "add_item":

            item_name = request.form.get("item_name")
            item_name = item_name.strip()
            quantity = request.form.get("quantity")
            location_id = request.form.get("location_list")


            if not item_name or not quantity or location_id == "Location":
                flash("Please fill out all fields")
                return redirect(url_for("views.add"))
            if quantity.isnumeric() == False or int(quantity) < 1:
                flash("Please enter a valid quantity")
                return redirect(url_for("views.add"))

            items = Item.query.filter_by(item_name=item_name).all()
            items = query_to_dict(items)
            if len(items) > 0:
                for item in items:
                    if item["location_id"] == int(location_id):
                        flash("Item already in location")
                        return redirect(url_for("views.add"))

            new_item = Item(item_name=item_name,
                            quantity=quantity, location_id=location_id)
            db.session.add(new_item)
            db.session.commit()
            flash("Item added")

            return redirect(url_for("views.index"))
        elif request.form["submitButton"] == "add_location":
            location_name = request.form.get("location_name")
            if not location_name:
                flash("Please fill out all fields")
                return redirect(url_for("views.add"))

            locations = Location.query.filter_by(name=location_name).all()

            if locations:
                flash("Location already exists")
                return redirect(url_for("views.add"))

            new_location = Location(location_name)
            db.session.add(new_location)
            db.session.commit()
            flash("Location added")
            return redirect(url_for("views.index"))
    else:
        locations = Location.query.all()
        locations = query_to_dict(locations)
        return render_template("add.html", locations=locations, user=current_user)


@views.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Edit inventory entries"""
    if request.method == "POST":

        if request.form["submitButton"] == "edit_item":

            item_id = request.form.get("item_list")
            quantity = request.form.get("quantity")
            location_id = request.form.get("location_list")

            if item_id == "Item" or not quantity or location_id == "Location":
                flash("Please fill out all fields")
                return redirect(url_for("views.edit"))

            if quantity.isnumeric() == False or int(quantity) < 1:
                flash("Please enter a valid quantity")
                return redirect(url_for("views.edit"))

            item_to_edit = Item.query.get(item_id)
            item_to_edit.quantity = quantity
            item_to_edit.location_id = location_id
            db.session.commit()

            return redirect(url_for("views.index"))

        elif request.form["submitButton"] == "edit_location":

            location_id = request.form.get("location_list_second")
            location_name = request.form.get("new_location_name")
            location_name = location_name.strip()

            if location_id == "Location" or not location_name:
                flash("Please fill out all fields")
                return redirect(url_for("views.edit"))

            location_to_edit = Location.query.get(location_id)
            location_to_edit.name = location_name
            db.session.commit()
            return redirect(url_for("views.index"))

    else:

        items = Item.query.all()
        items = query_to_dict(items)
        locations = Location.query.all()
        locations = query_to_dict(locations)
        return render_template("edit.html", items=items, locations=locations, user=current_user)


@views.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Delete inventory from database"""
    if request.method == "POST":

        if request.form["submitButton"] == "delete_item":

            item_id = request.form.get("delete_list")
            if item_id == "Item":
                flash("Please select an item to delete")
                return redirect(url_for("views.delete"))
            item = Item.query.get(item_id)

            if item:
                db.session.delete(item)
                db.session.commit()
                flash("Item deleted")
                return redirect(url_for("views.index"))
            else:
                flash("Item not found")
                return redirect(url_for("views.delete"))

        elif request.form["submitButton"] == "delete_location":

            location_id = request.form.get("delete_location_list")
            reassign = request.form.get("reassign")
            reassigned_location_id = request.form.get("reassign_location_list")

            if location_id == "Location":
                flash("Please select a location to delete")
                return redirect(url_for("views.delete"))

            if reassign == "off" and reassigned_location_id != "(Only for reassignment) Location":
                flash(
                    "Please check off the reassignment checkbox before selecting a new location")
                return redirect(url_for("views.delete"))

            if reassign == "on" and reassigned_location_id == "(Only for reassignment) Location":
                flash("Please select a location to reassign items to")
                return redirect(url_for("views.delete"))

            if reassign == "on" and int(reassigned_location_id) == int(location_id):
                flash("Please select a different location to reassign items to")
                return redirect(url_for("views.delete"))

            if reassign == "on":
                items_to_edit = Item.query.filter_by(
                    location_id=location_id).all()
                for item in items_to_edit:
                    item.location_id = reassigned_location_id
                    db.session.commit()

                location_to_delete = Location.query.get(location_id)
                db.session.delete(location_to_delete)
                db.session.commit()
                flash("Location deleted")
                return redirect(url_for("views.index"))

            items_to_delete = Item.query.filter_by(
                location_id=location_id).all()
            for item in items_to_delete:
                db.session.delete(item)
                db.session.commit()

            location_to_delete = Location.query.get(location_id)
            db.session.delete(location_to_delete)
            db.session.commit()
            flash("Location and associated items deleted")

            return redirect(url_for("views.index"))

    else:

        items = Item.query.all()
        items = query_to_dict(items)
        locations = Location.query.all()
        locations = query_to_dict(locations)
        return render_template("delete.html", items=items, locations=locations, user=current_user)

@views.route("/variance-calculator")
@login_required
def variance_calculator():
    """Calculate variance"""
    items = Item.query.all()
    items = query_to_dict(items)

    return render_template("variance_calculator.html", items=items, user=current_user)
