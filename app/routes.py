from flask import Blueprint, request, jsonify
from app import db
from .models.task import Task
from .models.goal import Goal
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#Decorator functions for error messages:
def task_not_found(func):
    def inner(task_id):
        if Task.query.get(task_id) is None:
            return jsonify(None), 404
        return func(task_id)
    #renames the function for each endpoint it's wrapping so there isn't the endpoint conflict
    inner.__name__ = func.__name__
    return inner

def goal_not_found(func):
    def inner(goal_id):
        if Goal.query.get(goal_id) is None:
            return jsonify(None), 404
        return func(goal_id)
    #renames the function for each endpoint it's wrapping so there isn't the endpoint conflict
    inner.__name__ = func.__name__
    return inner

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def tasks_index():
    sort_order = request.args.get('sort')
    if sort_order == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_order == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json()["task"])
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
@task_not_found
def single_task(task_id):
    task = Task.query.get(task_id)
    return jsonify(task.to_json()), 200

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return jsonify({"details":"Invalid data"}), 400
    
    new_task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_json()), 201

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
@task_not_found
def update_task(task_id):
    task = Task.query.get(task_id)
    form_data = request.get_json()
    task.title = form_data["title"]
    task.description = form_data["description"]
    task.completed_at = form_data["completed_at"]
    db.session.commit()
    return jsonify(task.to_json()), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
@task_not_found
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"details":f'Task {task.id} "{task.title}" successfully deleted'}), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
@task_not_found
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    # Slack
    post_message(f"Someone just completed the task {task.title}")
    return jsonify(task.to_json()), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
@task_not_found
def incomplete_task(task_id):
    task = Task.query.get(task_id)
    task.completed_at = None
    db.session.commit()
    return jsonify(task.to_json()), 200

#Helper function posting to slack
def post_message(message):
    path = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"}
    query_params = {"channel": "task-notifications",
                    "text": message
                    }
    requests.post(path, params=query_params, headers=headers)

# GOALS:
@goals_bp.route("", methods=["GET"], strict_slashes=False)
def goals_index():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
@goal_not_found
def single_goal(goal_id):
    goal = Goal.query.get(goal_id)
    return jsonify({"goal":goal.to_json()}), 200

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify({"details":"Invalid data"}), 400
    new_goal = Goal(title = request_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal":new_goal.to_json()}), 201

@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
@goal_not_found
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    form_data = request.get_json()
    goal.title = form_data["title"]
    db.session.commit()
    return jsonify({"goal":goal.to_json()}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
@goal_not_found
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({"details":f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200


# GOALS WITH TASKS
@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
@goal_not_found
def get_tasks_from_goal(goal_id):
    goal = Goal.query.get(goal_id)
    # Why does this line work?
    tasks = Task.query.filter_by(goal_id=goal.id)
    task_list = []
    for task in tasks:
        task_list.append(task.to_json())
## make individualized return so you don't mess up wave 5 trying to make this work
    return jsonify(goal.to_json()), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def post_tasks_to_goal(goal_id):
    request_body = request.get_json()
    # if "task_ids" not in request_body:
    #     return jsonify({"details":"Invalid data"}), 400
    task_ids = request_body["task_ids"]
    for id in task_ids:
        task = Task.query.get(id)
        # Once we set the task's goal_id attribute to the current goal, it automatically gets referenced from goal
        task.goal_id = goal_id
    db.session.commit()
    return jsonify({"id":int(goal_id), "task_ids":task_ids}), 200