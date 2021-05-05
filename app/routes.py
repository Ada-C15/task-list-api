from flask import Blueprint, request, make_response
from flask import jsonify
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():

    if request.method == "POST":

        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])
        
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": False
                }
        }), 201

    if request.method == "GET":

        tasks = Task.query.all()
        task_list = []

        for task in tasks:
            task_list.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            })
        
        return jsonify(task_list) # default 200 OK

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return "", 404 # make_response?  jsonify?

    if request.method == "GET":
        return jsonify({
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
        }})
    
    if request.method == "PUT":

        task_data = request.get_json()

        task.title = task_data["title"]
        task.description = task_data["description"]
        task.completed_at = task_data["completed_at"]

        db.session.commit()

        return jsonify({
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        })

    if request.method == "DELETE":

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "details": f"Task {task.task_id} \ {task.description} \ successfully deleted."
        })







