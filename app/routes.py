from app import db
from flask import request, Blueprint, make_response, jsonify
from app.models.task import Task
from sqlalchemy import desc, asc


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        order = request.args.get("sort")
        if order == "asc":
            tasks_query = Task.query.order_by(Task.title).all()
        else:
            tasks_query = Task.query.order_by(Task.title.desc())
        tasks_response = []
        for task in tasks_query:
            tasks_response.append({
                "id" : task.task_id,
                "title" : task.title,
                "description" : task.description,
                "is_complete" : bool(task.completed_at)
            })
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body.keys() or "description" not in request_body.keys() or "is_complete" not in request_body.keys():
            return make_response({"details": "Invalid data"}, 400)
        
        new_task = Task(
            title=request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"],
        )
        db.session.add(new_task)
        db.session.commit()

        return {"task":{
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)

            }}, 201

@tasks_bp.route("/<task_id>", methods = ["GET", "PUT", "DELETE", "PATCH"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    if request.method == "GET":
        return {"task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)

            }}
    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return {"task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)

            }}
    
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}
    
