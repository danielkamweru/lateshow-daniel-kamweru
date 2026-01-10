from flask import request, jsonify
from __init__ import create_app, db
from models import Episode, Guest, Appearance

app = create_app()

@app.route("/episodes", methods=["GET"])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([e.to_dict(only=("id", "date", "number")) for e in episodes]), 200

@app.route("/episodes/<int:id>", methods=["GET"])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    return jsonify(
        episode.to_dict(
            only=("id", "date", "number", "appearances"),
            rules=("-appearances.episode",)
        )
    ), 200

@app.route("/episodes/<int:id>", methods=["DELETE"])
def delete_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    db.session.delete(episode)
    db.session.commit()
    return jsonify({}), 204

@app.route("/guests", methods=["GET"])
def get_guests():
    guests = Guest.query.all()
    return jsonify([g.to_dict(only=("id", "name", "occupation")) for g in guests]), 200

@app.route("/appearances", methods=["POST"])
def create_appearance():
    data = request.get_json()
    try:
        appearance = Appearance(
            rating=data["rating"],
            episode_id=data["episode_id"],
            guest_id=data["guest_id"]
        )
        db.session.add(appearance)
        db.session.commit()
        
        return jsonify(
            appearance.to_dict(
                only=(
                    "id",
                    "rating",
                    "episode_id",
                    "guest_id",
                    "episode",
                    "guest"
                )
            )
        ), 201
    
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5555)
    1