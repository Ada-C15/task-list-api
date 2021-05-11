from app import db
from flask import Blueprint, request, jsonify
from app.models.goal import Goal


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body.keys():
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(title = request_body["title"])
    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_json()
    }, 201

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_goal():
    title_from_url = request.args.get("title")

    if title_from_url:
        goals = Goal.query.filter_by(title = title_from_url)

    goals = Goal.query.all()
    
    goals_response = []
    for goal in goals:
        tasks_response.append(goal.to_json())

    return jsonify(goals_response), 200