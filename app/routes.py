from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
            tasks = Task.query.all()
            tasks_response = []
            for task in tasks:
                tasks_response.append({
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False})
            return jsonify(tasks_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
        db.session.add(new_task)
        db.session.commit()

        return make_response(
        { "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
            }}, 201)

@tasks_bp.route("/<task_id>", methods = ["GET", "PUT"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
            return make_response("", 404)
    if request.method == "GET":
        return {
        "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False    
        }
    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return make_response(jsonify({
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False}))
        
                
