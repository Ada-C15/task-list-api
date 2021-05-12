from flask.json import jsonify
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, request
from sqlalchemy import desc

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_new_goal():
    new_goal_data = request.get_json()
    if new_goal_data.keys() >= {"title"}:
        new_goal = Goal(**new_goal_data)
        db.session.add(new_goal)
        db.session.commit()
        return {"goal": new_goal.goal_to_json()}, 201
    return {"details": "Invalid data"}, 400

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_goals():    
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(Goal.goal_id).all()
    elif sort_query == "desc":
        goals = Goal.query.order_by(desc(Goal.goal_id)).all()
    elif sort_query:
        return {
            "details": f'Sort by "{sort_query}" is not an option'
        }, 404
    else:    
        goals = Goal.query.all()

    response_body = [goal.goal_to_json() for goal in goals]
    return jsonify(response_body), 200

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_single_goal(goal_id):
    if not is_int(goal_id):
        return {
        "details": "Task id must be an integer"
        }, 404
    
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify(None), 404 

    if request.method == "GET":
        return {"goal": goal.goal_to_json()}, 200
    elif request.method == "PUT":
        replace_goal_data = request.get_json()
        if replace_goal_data.keys() >= {"title"}:
            goal.title = replace_goal_data["title"]
            db.session.commit()
            return {"goal": goal.goal_to_json()}, 200
        else:
            return {"details": "Invalid data"}, 400
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return {
            "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
        }

@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def set_goal_to_tasks(goal_id):
    if not is_int(goal_id):
        return {
        "details": "Task id must be an integer"
        }, 404
    
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify(None), 404
    
    if request.method == "POST":
        tasks_data = request.get_json()
        for task_id in tasks_data["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal.goal_id
        db.session.commit()
        return {
            "id": goal.goal_id,
            "task_ids": tasks_data["task_ids"]
        }, 200
    
@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_tasks_by_goal(goal_id):
    if not is_int(goal_id):
        return {
        "details": "Task id must be an integer"
        }, 404
    
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify(None), 404
    
    tasks = Task.query.filter_by(goal_id=goal.goal_id)
    tasks_response = [task.task_to_json() for task in tasks]
    response_body = goal.goal_to_json()
    response_body["tasks"] = tasks_response
    return response_body, 200
