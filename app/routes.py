from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks") 

@tasks_bp.route("", methods=["POST","GET"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()
        if 'title' in request_body and 'description' in request_body and 'completed_at' in request_body: 
            new_task = Task(title=request_body["title"],
                            description=request_body["description"],
                            completed_at = request_body["completed_at"])
            db.session.add(new_task)
            db.session.commit()

            task_response = {
                "id": new_task.task_id,
                "title": new_task.title,    
                "description": new_task.description,
                "is_complete": bool(new_task.completed_at)
                }
            response = {"task": task_response}
            return jsonify(response), 201
        else:
            return make_response ({"details": "Invalid data"},400)

    elif request.method == "GET":
        sort_by_title = request.args.get("sort")
        if sort_by_title == "asc": 
            tasks = Task.query.order_by(Task.title.asc())
        elif sort_by_title == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        
        else:
            tasks = Task.query.all()
    
        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,    
                "description": task.description,
                "is_complete": bool(task.completed_at)
                })
        return jsonify(tasks_response),200

@tasks_bp.route("/<task_id>", methods=["GET","PUT","DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("",404)

    if request.method == "GET":
        task_response = {
            "id": task.task_id,
            "title": task.title,    
            "description": task.description,
            "is_complete": bool(task.completed_at)
                }
        response = {"task": task_response}
        return jsonify(response), 200

    elif request.method == "PUT":      
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]

        db.session.commit()
        
        task_response = {
            "id": task.task_id,
            "title": task.title,    
            "description": task.description,
            "is_complete": bool(task.completed_at)
                }
        response = {"task": task_response}
        return jsonify(response), 200
        
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        delete_text = f"Task {task.task_id} \"{task.title}\" successfully deleted"
        response = {"details":delete_text}
        return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("",404)
    
    task.completed_at = datetime.datetime.now()
    db.session.commit()

    task_response = {
        "id": task.task_id,
        "title": task.title,    
        "description": task.description,
        "is_complete": bool(task.completed_at)
        }
    response = {"task": task_response}
    return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("",404)
    
    task.completed_at = None
    db.session.commit()

    task_response = {
        "id": task.task_id,
        "title": task.title,    
        "description": task.description,
        "is_complete": bool(task.completed_at)
        }
    response = {"task": task_response}
    return jsonify(response), 200