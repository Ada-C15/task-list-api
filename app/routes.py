from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET","POST"])
def handle_tasks():
    if request.method == "GET":
        sort = request.args.get("sort")

        if sort == "asc":
            tasks = Task.query.order_by(asc("title"))
        
        elif sort == "desc":
            tasks = Task.query.order_by(desc("title"))
        
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

        if "title" not in request_body.keys() or "description" not in request_body.keys() or "completed_at" not in request_body.keys():
            invalid_data = {"details": "Invalid data"}
            return make_response(invalid_data, 400)

        else:    
            new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=None)
            
            db.session.add(new_task)
            db.session.commit()

            return make_response({"task": new_task.make_json()}, 201)

@tasks_bp.route("/<task_id>", methods= ["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    elif request.method == "GET":
        return make_response({"task": task.make_json()})

    elif request.method == "PUT":
        request_body = request.get_json()

        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]

        db.session.commit()

        return make_response({"task": task.make_json()}) 
        
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        return {
            "details": (f"Task {task.task_id} \"{task.title}\" successfully deleted")
        }

