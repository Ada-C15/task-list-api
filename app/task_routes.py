from flask.json import jsonify
from app import db
from app.models.task import Task
from flask import Blueprint, request
from sqlalchemy import desc
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def handle_tasks():
    if request.method == "POST":
        new_task_data = request.get_json()
        if new_task_data.keys() >= {"title", "description", "completed_at"}:
            new_task = Task(
                title=new_task_data["title"],
                description=new_task_data["description"],
                completed_at=new_task_data["completed_at"]
            )
            db.session.add(new_task)
            db.session.commit()
            return {"task": new_task.to_json()}, 201
        else:
            return {"details": "Invalid data"}, 400
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title).all()
        elif sort_query == "desc":
            tasks = Task.query.order_by(desc(Task.title)).all()
        else:
            tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.to_json())
        return jsonify(tasks_response), 200

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_single_task(task_id):
    if not is_int(task_id):
        return jsonify(None), 404

    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    elif request.method == "GET":
        return {"task": task.to_json()}, 200
    elif request.method == "PUT":
        replace_task_data = request.get_json()
        if replace_task_data.keys() >= {"title", "description", "completed_at"}:
            task.title = replace_task_data["title"]
            task.description = replace_task_data["description"]
            task.completed_at = replace_task_data["completed_at"]
            db.session.commit()
            return {"task": task.to_json()}, 200
        else: 
            return {"details": "Invalid data"}, 400
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {
            "details": f'Task {task.id} "{task.title}" successfully deleted'
        }

@tasks_bp.route("/<task_id>/<task_stutas>", methods=["PATCH"], strict_slashes=False)
def update_task_status(task_id, task_stutas):
    if not is_int(task_id):
        return jsonify(None), 404

    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    elif task_stutas == "mark_complete":
        task.completed_at = datetime.utcnow()
        db.session.commit()
        slack_api_url = "https://slack.com/api/chat.postMessage"
        task_params = {
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}"
        }
        task_autho = {"Authorization": os.environ.get("SLACK_CHAT_POST_MESSAGE_TOKEN")}
        requests.post(slack_api_url, json=task_params, headers=task_autho)
        return  {"task": task.to_json()}, 200
    elif task_stutas == "mark_incomplete":
        task.completed_at = None
        db.session.commit()
        return  {"task": task.to_json()}, 200

