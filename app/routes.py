from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def is_complete_helper_function():
    is_complete = True
    if Task.completed_at is None:
        is_complete == False
        return is_complete
    else:
        is_complete == True
        return is_complete

@tasks_bp.route("", methods = ["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title).all()
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
        else:
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
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return make_response({
        "details": "Invalid data"
    }, 400)
        else:
            new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
            db.session.add(new_task)
            db.session.commit()
            return make_response(
                    { "task": {
                    "id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": is_complete_helper_function()
                    }}, 201)
            


@tasks_bp.route("/<task_id>", methods = ["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
            return make_response("", 404)
    if request.method == "GET":
        return {"task":{
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False    
        }}
    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return make_response(jsonify({"task":{
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": is_complete_helper_function()}}))
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})) 



@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])  
def mark_complete(task_id): 
    task = Task.query.get(task_id)    
    form_data = request.get_json()
    if task is None:
            return make_response("", 404)
    if task.completed_at is None:
        task.completed_at = datetime.now()
        db.session.commit()   
        return make_response(jsonify({"task":{
                        "id": task.task_id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": True}})) 
    else:
        task.completed_at = datetime.now()
        db.session.commit()   
        return make_response(jsonify({"task":{
                        "id": task.task_id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": True}}))

@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])  
def patch_incomplete_on_completed_task(task_id): 
    task = Task.query.get(task_id)    
    form_data = request.get_json()
    if task is None:
            return make_response("", 404)
    if task.completed_at is None:
        db.session.commit()   
        return make_response(jsonify({"task":{
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False}}))
    else:
        task.completed_at = None
        db.session.commit()   
        return make_response(jsonify({"task":{
                        "id": task.task_id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": False}}))       

