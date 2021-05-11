from app import db
from flask import Blueprint, request, jsonify
from app.models.goal import Goal


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body.keys():
        return {"details": "Invalid data"}, 400
    
    new_goal = Task(title = request_body["title"])
    db.session.add(new_task)
    db.session.commit()

    return {
        "goal": new_goal.to_json()
    }, 201