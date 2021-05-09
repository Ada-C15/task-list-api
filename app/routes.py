from flask import request, Blueprint, make_response, jsonify
from app import db
from app.models.task import Task
from datetime import datetime
import os



tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "desc":
            tasks = Task.query.order_by((Task.title.desc()))
        elif sort_query == "asc":
            tasks = Task.query.order_by(Task.title)
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            tasks_response.append(task.dict_response())
        return jsonify(tasks_response)

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body\
            or "description" not in request_body\
                or "completed_at" not in request_body:
            return({"details":"Invalid data"}, 400)

        new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()

        return make_response({"task": new_task.dict_response()}, 201)



@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def single_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        return {"task": task.dict_response()}

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data['title']
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        
        db.session.commit()

        return jsonify({"task":task.dict_response()}), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        return {"details": 
                (f'Task {task.task_id} "{task.title}" successfully deleted')}

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = datetime.utcnow()
        
        db.session.commit()
        return {"task":task.dict_response()}
    else: 
        return make_response("", 404)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = None
        db.session.commit()
        return {"task":task.dict_response()}
    else:
        return make_response("", 404)


