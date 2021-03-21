import datetime as dt
import uuid

from flask import Flask, abort, jsonify, make_response, request

fake_database = None


def create_app():

    app = Flask(__name__)

    fake_database = dict()

    @app.route("/")
    def index():
        return "It works!"

    @app.route("/ales", methods=["GET", "POST"])
    def ales():
        if request.method == "POST":
            ale = request.json

            if ale["alcohol_by_volume"] < 0 or ale["alcohol_by_volume"] > 100:
                abort(422)

            ale["id"] = uuid.uuid4()
            ale["created_at"] = dt.datetime.utcnow()
            fake_database[ale["id"]] = ale
            return make_response(jsonify(ale), 201)
        else:
            return make_response(
                jsonify([v for k, v in fake_database.items()])
            )

    @app.route("/ales/<ale_id>", methods=["GET", "PUT", "DELETE"])
    def ale(ale_id):
        ale_id = uuid.UUID(ale_id)

        if ale_id not in fake_database:
            abort(404)

        if request.method == "PUT":
            ale = request.json
            ale["created_at"] = dt.datetime.utcnow()
            fake_database[ale_id] = ale
            return make_response(jsonify(ale))
        elif request.method == "GET":
            return make_response(jsonify(fake_database[ale_id]), 200)
        else:
            fake_database.pop(ale_id)
            return make_response("success", 204)

    return app
