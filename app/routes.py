from flask import Blueprint, request, jsonify
from app import db
from .models.task import Task
from .models.goal import Goal
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#---------------------# HELPER FUNCTIONS #---------------------#

def invalid_input():
    return jsonify({"details":"Invalid data"}), 400

def post_to_slack(message):
    path = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"}
    query_params = {"channel": "task-notifications",
                    "text": message
                    }
    requests.post(path, params=query_params, headers=headers)

#---------------------# DECORATORS #---------------------#

def task_not_found(func):
    def inner(task_id):
        if Task.query.get(task_id) is None:
            return jsonify(None), 404
        return func(task_id)
    #renames the function for each wrapped endpoint to avoid endpoint conflict
    inner.__name__ = func.__name__
    return inner

def goal_not_found(func):
    def inner(goal_id):
        if Goal.query.get(goal_id) is None:
            return jsonify(None), 404
        return func(goal_id)
    inner.__name__ = func.__name__
    return inner

def handle_missing_task_inputs(func):
    def inner(*args, **kwargs):
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return invalid_input()
        if not request_body["title"] or not request_body["description"]:
            return invalid_input()
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner

def handle_invalid_datetime(func):
    def inner(*args, **kwargs):
        request_body = request.get_json()
        # since request_body["completed"] is a string not a datetime, this tests for correct datetime format
        if request_body["completed_at"]:
            completed_at = str(request_body["completed_at"])
            try:
                datetime.strptime(completed_at, "%a, %d %B %Y %H:%M:%S %Z")
            except ValueError:
                return invalid_input()
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner

def handle_missing_goal_inputs(func):
    def inner(*args, **kwargs):
        request_body = request.get_json()
        if "title" not in request_body or not request_body["title"]:
            return invalid_input()
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner


#---------------------# TASK ENDPOINTS #---------------------#

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def tasks_index():
    sort_by = request.args.get('sort')
    if sort_by == "asc" or sort_by == "title":
        tasks = Task.query.order_by(Task.title)
    elif sort_by == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_by == "id":
        tasks = Task.query.order_by(Task.id)
    elif sort_by:
        return invalid_input()
    else:
        tasks = Task.query.all()
    tasks_response = [task.to_json()["task"] for task in tasks]
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
@task_not_found
def single_task(task_id):
    task = Task.query.get(task_id)
    return jsonify(task.to_json()), 200

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
@handle_missing_task_inputs
@handle_invalid_datetime
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_json()), 201

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
@task_not_found
@handle_missing_task_inputs
@handle_invalid_datetime
def update_task(task_id):
    task = Task.query.get(task_id)
    response_body = request.get_json()
    task.title = response_body["title"]
    task.description = response_body["description"]
    task.completed_at = response_body["completed_at"]
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
    post_to_slack(f"Someone just completed the task {task.title}")
    return jsonify(task.to_json()), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
@task_not_found
def incomplete_task(task_id):
    task = Task.query.get(task_id)
    task.completed_at = None
    db.session.commit()
    return jsonify(task.to_json()), 200


#---------------------# GOAL ENDPOINTS #---------------------#

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def goals_index():
    sort_by = request.args.get('sort')
    if sort_by == "asc" or sort_by == "title":
        goals = Goal.query.order_by(Goal.title)
    goals = Goal.query.all()
    goals_response = [goal.to_json() for goal in goals]
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
@goal_not_found
def single_goal(goal_id):
    goal = Goal.query.get(goal_id)
    return jsonify({"goal":goal.to_json()}), 200

@goals_bp.route("", methods=["POST"], strict_slashes=False)
@handle_missing_goal_inputs
def create_goal():
    request_body = request.get_json()
    new_goal = Goal(title = request_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal":new_goal.to_json()}), 201

@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
@goal_not_found
@handle_missing_goal_inputs
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


#---------------------# GOALS WITH TASK ENDPOINTS #---------------------#

@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
@goal_not_found
def get_tasks_from_goal(goal_id):
    goal = Goal.query.get(goal_id)
    #Only need this b/c I reconfigured .to_json() to drop "tasks" if empty (to pass previous tests) 
    if "tasks" not in goal.to_json():
        goal_return = goal.to_json()
        goal_return.update({"tasks": []})
        return jsonify(goal_return), 200
    return jsonify(goal.to_json()), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
@goal_not_found
def post_tasks_to_goal(goal_id):
    request_body = request.get_json()
    if "task_ids" not in request_body:
        return invalid_input()
    task_ids = request_body["task_ids"]
    for id in task_ids:
        task = Task.query.get(id)
        task.goal_id = int(goal_id)
    db.session.commit()
    return jsonify({
                "id":int(goal_id), 
                "task_ids":task_ids
                }), 200