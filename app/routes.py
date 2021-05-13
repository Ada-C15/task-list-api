from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
import datetime
from datetime import datetime, date, time, timezone
from dotenv import load_dotenv
import os
import requests
import json

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def is_complete_function(completed_at):
        if completed_at is not None:
            return True
        else:
            return False

def post_message_to_slack(text, blocks=None):
    requests.post('https://slack.com/api/chat.postMessage', 
    headers={'Authorization': f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"},
    data={'channel': f"{os.environ.get('SLACK_CHANNEL')}", 'text': text})

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def handle_tasks():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task(title= request_body["title"],
    description= request_body["description"],
    completed_at= request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": is_complete_function(new_task.completed_at)}}), 201


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def tasks_index():
    
    sort_query = request.args.get("sort")
    tasks_response = []
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))

        for task in tasks:
                tasks_response.append({
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": is_complete_function(task.completed_at)
                })
        return jsonify(tasks_response), 200

    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))

        for task in tasks:
                tasks_response.append({
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": is_complete_function(task.completed_at)
                })
        return jsonify(tasks_response), 200

    else:
        tasks = Task.query.all()
    
        if tasks is None:
            return jsonify(tasks_response), 200
    
        else:
            for task in tasks:
                tasks_response.append({
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": is_complete_function(task.completed_at)
                })
            return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def handle_single_task(task_id):

    task = Task.query.get_or_404(task_id)
    
    if task.goal_id:
        return jsonify({"task": {
        "id": task.task_id,
        "goal_id": task.goal_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete_function(task.completed_at)}}), 200

    return jsonify({"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete_function(task.completed_at)}}), 200
    

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_single_task(task_id):
    task = Task.query.get_or_404(task_id)

    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()

    return jsonify({"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete_function(task.completed_at)}}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details" : f"Task {task.task_id} \"{task.title}\" successfully deleted"}), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_single_task_complete(task_id):
    task = Task.query.get_or_404(task_id)

    task.completed_at = datetime.now()

    db.session.commit()

    post_message = f"Someone just completed the task {task.title}."
    post_message_to_slack(post_message)

    return jsonify({"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete_function(task.completed_at)}}), 200

    
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_single_task_incomplete(task_id):
    task = Task.query.get_or_404(task_id)

    task.completed_at = None

    db.session.commit()

    return jsonify({"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete_function(task.completed_at)}}), 200


@goals_bp.route("", methods=["POST"], strict_slashes=False)
def handle_goals():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_goal = Goal(title= request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": {"id": new_goal.goal_id,
        "title": new_goal.title}}), 201


@goals_bp.route("", methods=["GET"], strict_slashes=False)
def goals_index():
    
    goals = Goal.query.all()
    goals_response = []
    
    if goals is None:
            return jsonify(goals_response), 200

    else:
        for goal in goals:
            goals_response.append({
                "id": goal.goal_id,
                "title": goal.title})
        return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def handle_single_goal(goal_id):

    goal = Goal.query.get_or_404(goal_id)
    
    return jsonify({"goal": {
        "id": goal.goal_id,
        "title": goal.title}}), 200


@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_single_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    request_body = request.get_json()
    
    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": {
        "id": goal.goal_id,
        "title": goal.title}}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details" : f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def handle_goals_tasks(goal_id):
    request_body = request.get_json()
    
    goal = Goal.query.get_or_404(goal_id)

    tasks = request_body["task_ids"]

    for task in tasks:
        task_to_update = Task.query.get(task) 
        task_to_update.goal_id = goal_id

    db.session.commit()

    return jsonify({"id": goal.goal_id,
        "task_ids": tasks}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def index_goals_tasks(goal_id):
    
    goal = Goal.query.get_or_404(goal_id)

    goal_tasks = goal.tasks

    return_list_of_tasks = []
    for task in goal_tasks:
        return_list_of_tasks.append({"id": task.task_id,
                    "goal_id": task.goal_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": is_complete_function(task.completed_at)
                })

    return jsonify({"id": goal.goal_id,
        "title": f"{goal.title}",
        "tasks": return_list_of_tasks}), 200