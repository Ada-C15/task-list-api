from flask.json import jsonify
from app import db
from app.models.goal import Goal
from flask import Blueprint, request

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST","GET"], strict_slashes=False)
def handle_goals():
    if request.method == "POST":
        new_goal_data = request.get_json()
        if new_goal_data.keys() >= {"title"}:
            new_goal = Goal(title=new_goal_data["title"])
            db.session.add(new_goal)
            db.session.commit()
            return {"goal": new_goal.to_json()}, 201
        return {"details": "Invalid data"}, 400
    if request.method == "GET":
        goals = Goal.query.all()
        response_body = []
        for goal in goals:
            response_body.append(goal.to_json())
        return jsonify(response_body), 200

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_single_goal(goal_id):
    if not is_int(goal_id):
        return jsonify(None), 404
    
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify(None), 404 
    elif request.method == "GET":
        return {"goal": goal.to_json()}, 200
    elif request.method == "PUT":
        replace_goal_data = request.get_json()
        if replace_goal_data.keys() >= {"title"}:
            goal.title = replace_goal_data["title"]
            db.session.commit()
            return {"goal": goal.to_json()}, 200
        else:
            return {"details": "Invalid data"}, 400
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return {
            "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
        }