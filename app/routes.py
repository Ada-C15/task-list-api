from flask import Blueprint
import flask_migrate
from app import db 
from app.models.task import Task 
from flask import request, Blueprint, make_response 
from flask import jsonify


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def handle_task():
    if request.method == "GET":  
        tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            })
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        new_task = Task(title = request_body["title"], 
                    description = request_body["description"], 
                    completed_at = request_body["completed_at"])
        db.session.add(new_task)
        db.session.commit() 

        return {
            "task":{
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": False
    }}, 201


@tasks_bp.route("/<task_id>", methods=["GET", "PUT"], strict_slashes=False)
def task_by_id(task_id):
    task = Task.query.get(task_id)
    if request.method == "GET":
        if task:
            return {
                "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False}
        }, 200

        else:
            return (f"None", 404)
    if request.method == "PUT":
        if task:
            request_body = request.get_json()
            task.title = request_body["title"]
            task.description = request_body["description"]
            task.completed_at = request_body["completed_at"]
            db.session.commit()
            return { "task": {
                        "id": task.task_id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": False
            }}, 200
        else:
            return (f"None", 404)
    
