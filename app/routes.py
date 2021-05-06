from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify
from sqlalchemy import asc, desc
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    order_query = request.args.get("sort")
    if order_query:
        if order_query == "asc":
            tasks = Task.query.order_by(asc(Task.title))
            # tasks = {"a", "b", "c"}
        elif order_query == "desc":
            tasks = Task.query.order_by(desc(Task.title))
            # tasks = {"d", "e", "f"}
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    
    return jsonify(tasks_response), 200
  
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return {"task": task.to_json()}, 200
    else:
        return jsonify(None), 404
      

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    if all(key in request_body for key in ("title", "description", "completed_at")):
        new_task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = request_body["completed_at"])
        
        db.session.add(new_task)
        db.session.commit()

        return {
                "task": new_task.to_json()
        }, 201
    else:
        return {"details": "Invalid data"}, 400
      
@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return {
                "task": task.to_json()
        }, 200
    else:
        return jsonify(None), 404

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return {
              "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }
    else:
        return jsonify(None), 404
      
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = datetime.utcnow()
        db.session.commit()
        return {
        "task": task.to_json()
        }, 200
    else:
        return jsonify(None), 404
      
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = None
        db.session.commit()
        return {
        "task": task.to_json()
        }, 200
    else:
        return jsonify(None), 404


      

    
      
