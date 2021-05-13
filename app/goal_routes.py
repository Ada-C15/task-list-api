from app import db
from flask import Blueprint, request, jsonify
from app.models.goal import Goal
from app.models.task import Task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def add_tasks(goal_id):
    request_body = request.get_json()

    tasks = []
    for task_id in request_body["task_ids"]:
        tasks.append(Task.query.get(task_id))

    goal = Goal.query.get(goal_id)

    goal.tasks.extend(tasks)

    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }, 200

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
        goals_response.append(goal.to_json())

    return jsonify(goals_response), 200


def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False


@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes = False)
def get_goal_by_id(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return ("", 404)

    if not is_int(goal_id):
        return ("", 404)

    return {"goal": goal.to_json()}, 200


@goals_bp.route("/<goal_id>", methods = ["PUT"], strict_slashes = False)
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return ("", 404)

    form_data = request.get_json()

    goal.title = form_data["title"]

    db.session.commit()

    return {"goal": goal.to_json()}, 200


@goals_bp.route("/<goal_id>", methods = ["DELETE"], strict_slashes = False)
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return ("", 404)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}, 200