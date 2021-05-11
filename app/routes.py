from flask import request, Blueprint, make_response
from app import db
from flask import jsonify
from .models.task import Task
from .models.goal import Goal
from datetime import datetime
import requests
import os

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@task_bp.route("", methods=["POST"], strict_slashes=False)
def add_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return jsonify({
        "details": "Invalid data"
        }), 400
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
            "task":{
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.convert_complete()
    }}), 201

@task_bp.route("", methods=["GET"], strict_slashes=False)
def task_index():
    tasks = Task.query.all()
    sort_order = request.args.get("sort")
    task_response = []
    for task in tasks:
            task_response.append(task.to_json())
    
    if sort_order == "asc":
        task_response = sorted(task_response, key=lambda k: k['title'])
    if sort_order == "desc":
        task_response = sorted(task_response, key=lambda k: k['title'], reverse = True)

    return jsonify(task_response), 200


@task_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_task(task_id):
    task = Task.query.get(task_id)
    if task: 
        return jsonify({
            "task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.convert_complete()
            }
            }), 200
    return "", 404


@task_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return jsonify({
            "task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.convert_complete()
            }
            }), 200
    return "", 404

@task_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({
            "details": (f'Task {task.task_id} "{task.title}" successfully deleted')
        }), 200
    return "", 404

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete_task(task_id):
    task = Task.query.get(task_id)
    if task: # only send part that i am substituting 
        task.completed_at = datetime.utcnow()   #add current date using datetime method
        db.session.commit()

        SLACK_ENDPOINT = "https://slack.com/api/chat.postMessage"
        api_key = os.environ.get("SLACK_API_KEY")
        channel_id = "C021G7PULMS"

        query_params = {
            "token": api_key,
            "channel": channel_id,
            "text": f"Someone just completed the task {task.title}"
        }
        requests.post(SLACK_ENDPOINT, data=query_params)

        return jsonify({
            "task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.convert_complete()
            }
            }), 200
    return "", 404    

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = None
    # only send part that i am substituting 
    # need to refractor to make patch all fit on one line
        db.session.commit()
        return jsonify({
            "task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.convert_complete()
            }
            }), 200
    return "", 404    

@goal_bp.route("", methods=["POST"], strict_slashes=False)
def add_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify({
        "details": "Invalid data"
        }), 400

    new_goal= Goal(title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({
            "goal":{
            "id": new_goal.goal_id,
            "title": new_goal.title
    }}), 201

@goal_bp.route("", methods=["GET"], strict_slashes=False)
def goal_index():
    goals = Goal.query.all()
    goal_response = []
    for goal in goals:
            goal_response.append(goal.to_json())

    return jsonify(goal_response), 200

@goal_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal: 
        return jsonify({
            "goal":{
            "id": goal.goal_id,
            "title": goal.title
            }
            }), 200
    return "", 404

@goal_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        form_data = request.get_json()
        goal.title = form_data["title"]
        db.session.commit()
        return jsonify({
            "goal":{
            "id": goal.goal_id,
            "title": goal.title
            }
            }), 200
    return "", 404

@goal_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        db.session.delete(goal)
        db.session.commit()
        return jsonify({
            "details": (f'Goal {goal.goal_id} "{goal.title}" successfully deleted')
        }), 200
    return "", 404

@goal_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def assign_goal_to_tasks(goal_id):
    goal = Goal.query.get(goal_id)
    request_body = request.get_json()
    task_list = request_body["task_ids"]

    for task_id in task_list:
        task = Task.query.get(task_id)
        if task:
            task.goal_id = goal_id
    
    return jsonify({
        "id": goal.goal_id,
        "task_ids": task_list
    }), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_tasks_for_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        task_found = Task.query.filter_by(goal.goal_id)

        if task_found:
            return jsonify({
                "id": goal.goal_id,
                "title": goal.title,
                "tasks":[
                    {
                        "id": task_found.task_id,
                        "goal_id": task_found.goal_id,
                        "title": task_found.title,
                        "description": task_found.description,
                        "is_complete": task_found.convert_complete()
                    }]
            }), 200
    return "", 404 