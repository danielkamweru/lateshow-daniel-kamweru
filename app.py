from flask import request, jsonify
from . import create_app, db
from . models import Episode,Guest, Appearances

app = create_app()
@app.route("/episodes", methods=["GET"])
def get_episodes():
    espisodes = Episode.query.all()
    return jsonify([e.to_dict(only=("id","date", "number")) for e in episodes]), 200
@app.route("/episodes/<int:id>", methods=["GET"])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error":"Episode not found"}), 404

    return jsonify(
        episode.to_dict(
            only=("id", "date", "number", "appearances"),
            rules=("-appearances.episode",)
        )
    ), 200