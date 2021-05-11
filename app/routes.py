from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify, Response
from datetime import datetime
from sqlalchemy import desc, asc
import os
import requests

#WAVE 1
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    
    if ("title" not in request_body or "description" not in request_body \
        or "completed_at" not in request_body):
        return jsonify({"details":"Invalid data"}),400
    
    else:
        new_task = Task(title = request_body["title"],
                        description = request_body["description"],
                        completed_at = request_body["completed_at"])
    
        db.session.add(new_task)
        db.session.commit()
        return {"task": new_task.to_json()}, 201

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_saved_tasks():

#WAVE 2    
    sort_by_title = request.args.get("sort")
    if sort_by_title == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_by_title == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):

    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    task = Task.query.get(task_id)
    if task:
        return {"task": task.to_json()}, 200
    else:
        return Response("",status=404)
    
@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    
    if task == None:
        return Response("", status=404)
    
    if task: 
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()
        return {"task": task.to_json()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)    
def delete_single_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return Response("", status=404)

    if task:
        db.session.delete(task)
        db.session.commit()

        return {
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200

#WAVE 3
@tasks_bp.route("/<task_id>/<task_completion>", methods=["PATCH"], strict_slashes=False)
def patch_task(task_id, task_completion):
    
    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    task = Task.query.get(task_id)

    if task == None:
        return Response("", status=404)

    elif task_completion == 'mark_complete':
        task.completed_at = datetime.today()

        url_path = "https://slack.com/api/chat.postMessage"
        SLACK_API_KEY = os.environ.get("SLACK_API_KEY")

        header = {
            "Authorization": f"Bearer {SLACK_API_KEY}"
            }

        query_params = {
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}"
        }

        requests.post(url_path, params=query_params, headers=header)

    else: 
        task.completed_at = None

    db.session.commit()
    return {"task": task.to_json()}, 200