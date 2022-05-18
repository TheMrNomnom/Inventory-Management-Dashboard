from flask import Blueprint, request, jsonify
from flask_login import login_required
from .models import Item, Location

endpoints = Blueprint("endpoints", __name__)

@endpoints.route("/item_info")
@login_required
def item_info():
    """Return all item info"""
    item_id = request.args.get("item_id")
    item_row = Item.query.get(item_id)
    item = []
    item.append(item_row.to_dict())
    return jsonify(item)

@endpoints.route("/location_info")
@login_required
def location_info():
    """Return location of item"""
    item_id = request.args.get("item_id")
    location_row = Location.query.join(Item).filter(Item.id == item_id).first()
    location = []
    location.append(location_row.to_dict())
    return jsonify(location)