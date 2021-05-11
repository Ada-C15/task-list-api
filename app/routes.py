from flask import current_app, Blueprint, make_response, jsonify, request, Response
from app import db
from app.models.task import Task
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import re
# from sqlachemy import asc, desc
load_dotenv()

PATH = "https://slack.com/api/chat.postMessage"

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def post_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({
            "details": "Invalid data"
        }, 400)

    else: 
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()

        return make_response({
            "task":{
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": bool(new_task.completed_at)
            }
        }, 201)

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_tasks():
    if request.args.get('sort'):
        if request.args.get('sort') == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif request.args.get('sort') == "desc":
            tasks= Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })

    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_one_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    if request.method == "GET":
        return {"task":{
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}, 200        
    elif request.method == "PUT":
        form_data = request.get_json()  #what is request.get_json? 
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return make_response({"task":{
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}, 200)
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200


@tasks_bp.route("/<task_id>/<completion>", methods=["PATCH"], strict_slashes=False)
def update_time(task_id, completion):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    form_data = request.get_json() 

    if completion == "mark_complete":
        task.completed_at = datetime.utcnow()
        query_params = {
            
            "channel": "task-notifications",
            "text" : f"Someone just completed the task {task.title}"
        }
        authorization = os.environ.get('API_KEY')
        headers = {"Authorization" : f"Bearer {authorization}"}

        response = requests.post(PATH, params=query_params, headers=headers)


    elif completion == "mark_incomplete":
        task.completed_at = None
        
    db.session.commit()

    return make_response({"task":{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
    }}, 200)

