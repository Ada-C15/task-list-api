from flask import request, Blueprint, make_response, jsonify

from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix= "/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def create_task():

    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        else:
            new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])

            db.session.add(new_task)
            db.session.commit()

            return make_response({
                "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": new_task.task_completed()
                }
            }, 201)
    
    elif request.method == "GET":
        tasks = Task.query.all()
        tasks_response = []

        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.task_completed()
            })
        return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def specific_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response(), 404
    
    elif request.method == "GET":
        return jsonify({
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.task_completed()
            }
        }), 200

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()

        return jsonify({
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.task_completed()
            }
        }), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200 





        




