from app import db
from .models.task import Task
from flask import request, Blueprint, make_response, jsonify
from sqlalchemy import desc, asc
import datetime
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title)
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
            })
        return jsonify(tasks_response)

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body\
            or "completed_at" not in request_body:
            return ({
                "details": "Invalid data"
            }, 400)
        else:
            new_task = Task(title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"])

            db.session.add(new_task)
            db.session.commit()

            return make_response({
                "task": {
                    "id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": new_task.is_complete()
            }}, 201)

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        if task.task_id:
            return {
                "task": {
                    "id": task.task_id,
                    # "task_id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": task.is_complete()
            }}
        else:
            return {
                "task": {
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": task.is_complete()
            }}
    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()
        
        headers = {"Authorization": os.environ.get("SLACK_KEY")}
        data = {
        "channel": "C021BV8A5V0", 
        "text": f"Someone just completed the task {task.title}"
        }
        
        requests.patch('https://slack.com/api/chat.postMessage',
        headers=headers, data=data)


        return {
                "task": {
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": task.is_complete()
            }}
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {
            "details": (f'Task {task.task_id} "{task.title}" successfully deleted')
        }
        
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    task.completed_at = None
    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False 
        }
    }
    
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    task.completed_at = datetime.datetime.now()
    db.session.commit()



    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True 
        }
    }
