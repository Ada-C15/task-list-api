from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from sqlalchemy import desc, asc 
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():

    if request.method == "GET":
        order_query = request.args.get("sort")
        if order_query == "asc":
            tasks = Task.query.order_by(asc(Task.title))
        elif order_query == "desc":
            tasks = Task.query.order_by(desc(Task.title))
        else:
            tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.to_dict())
        return make_response(jsonify(tasks_response), 200)

    else: 
        request_body = request.get_json()
        if "title" in request_body and "description" in request_body and "completed_at" in request_body:
            new_task = Task(title = request_body["title"],
                            description = request_body["description"],
                            completed_at=request_body["completed_at"])
            db.session.add(new_task)
            db.session.commit()
            return make_response({"task": new_task.to_dict()}, 201) 
        else:
            return make_response({"details": "Invalid data"}, 400)


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task:
        if request.method == "GET":
            return {"task": task.to_dict()}, 200

        elif request.method == "PUT":
            form_data = request.get_json()
            task.title = form_data["title"]
            task.description = form_data["description"]
            task.completed_at = form_data["completed_at"]
            db.session.commit()
            return make_response({"task": task.to_dict()}, 200)
        
        elif request.method == "DELETE":
            db.session.delete(task)
            db.session.commit()
            return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200)
    else:
        return make_response("", 404)

@tasks_bp.route("/<task_id>/<mark_info>", methods=["PATCH"])
def handle_task_completion(task_id, mark_info):
    task = Task.query.get(task_id)
    if task:
        if mark_info == "mark_incomplete":
            task.completed_at = None
            db.session.commit()
            return make_response({"task": task.to_dict()}, 200)
        elif mark_info == "mark_complete":
            task.completed_at = datetime.utcnow()
            db.session.commit()
            return make_response({"task": task.to_dict()}, 200)
    else:
        return make_response("", 404)


