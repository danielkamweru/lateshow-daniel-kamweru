from flask import request, jsonify
from . import create_app, db
from . models import Episode,Guest, Appearances

app = create_app()
@app.route("/episodes", methods=["GET"])
def get_episodes():
    espisodes = Episode.query.all()
    return jsonify([e.to_dict(only=("id","date", "number")) for e in episodes]), 200

