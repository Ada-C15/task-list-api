from app import db
from .models.task import Task
from flask import request, Blueprint, make_response, jsonify
from sqlalchemy import desc, asc

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST", "GET"])
def tasks():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        else:
            new_task = Task(title = request_body["title"],
                        description = request_body["description"],
                        completed_at = request_body["completed_at"])
            db.session.add(new_task)
            db.session.commit()

            return jsonify({"task":new_task.to_dict()}), 201

    elif request.method == "GET":
        sort_by = request.args.get("sort")
        if sort_by == "asc": 
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif sort_by == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
        else: 
            tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.to_dict())

        return jsonify(tasks_response), 200

@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response(), 404
    
    elif request.method == "GET":
        return jsonify({"task":task.to_dict()}), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}),200

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()

        return jsonify({"task":task.to_dict()}), 200



