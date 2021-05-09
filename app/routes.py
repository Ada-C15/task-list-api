from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify, Response
from datetime import datetime
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    
    if "title" not in request or "description" not in request_body \
        or "completed_at" not in request_body:
        return {
            "details": "Invalid Data"
        }, 400
    
    new_task = Task(title = request_body["title"],
                        description = request_body["description"],
                        completed_at = request_body["completed_at"])
    
    db.session.add(new_task)
    db.session.commit()

    return task.to_json(), 201

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_saved_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json() )
    
    return jsonify(tasks_response), 200

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_no_saved_tasks():
    tasks = Task.query.all()
    
    if tasks == []:
        return jsonify(tasks), 200

@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):

    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    task = Task.query.get(task_id)
    if task:
        return task.to_json(), 200
    
    return 404

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    
    if task == None:
        return Response("", status=404)
    
    if task: 
        form_data = request.get_json()

        task.name = form_data["name"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()
        return 200

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)    
def delete_single_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return Response("", status=404)

    if task:
        db.session.delete(task)
        db.session.commit()

        return {
            "details": f"Task {task.id}, {task.description} was successfully deleted", 
            "success": False
        }, 200
