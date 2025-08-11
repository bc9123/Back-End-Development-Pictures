from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    pic = next((p for p in data if p.get("id") == id), None)
    if pic is not None:
        return jsonify(pic), 200
    return jsonify({"message": "Not Found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    body = request.get_json(silent=True) or {}
    pic_id = body.get("id")
    if pic_id is None:
        return jsonify({"Message": "id required"}), 400

    if any(p.get("id") == pic_id for p in data):
        return jsonify({"Message": f"picture with id {pic_id} already present"}), 302

    data.append(body)
    return jsonify(body), 201
######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id: int):
    body = request.get_json(silent=True) or {}
    pic = next((p for p in data if p.get("id") == id), None)
    if pic is None:
        return jsonify({"message": "picture not found"}), 404

    body.pop("id", None)
    pic.update(body)
    return jsonify(pic), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id: int):
    for i, p in enumerate(data):
        if p.get("id") == id:
            data.pop(i)
            return ("", 204)
    return jsonify({"message": "picture not found"}), 404
