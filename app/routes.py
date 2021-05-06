from flask import Blueprint
from app import db
from app.models.task import Task
from flask import request
from flask import request, Blueprint, make_response
from flask import jsonify
from sqlalchemy import asc, desc




tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def tasks():
    
    if request.method == "GET":
        task_order = request.args.get("sort")
        if task_order == None:
            tasks = Task.query.all() # get all items in list
        elif task_order == "asc":
            tasks = Task.query.order_by(asc(Task.title))
        elif task_order == "desc":
            tasks = Task.query.order_by(desc(Task.title))




        tasks_response = []
        for task in tasks:
            complete=task.complete_helper()
            tasks_response.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": complete
            })
        return jsonify(tasks_response)

    
    else:
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)
            
        task = Task(title = request_body["title"],
                            description = request_body["description"],
                            completed_at = request_body["completed_at"])
        

        db.session.add(task)
        db.session.commit()

        complete=task.complete_helper()
        
        return make_response({
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": complete
                }}), 201      

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)

def handle_task(task_id):
    

    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        complete=task.complete_helper()
        return ({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": complete
        }}), 200

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        complete=task.complete_helper()
        return ({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": complete
        }})

    

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": (f"Task {task.id} \"Go on my daily walk 🏞\" successfully deleted")})
    
    
    return {
        "message": f"Task with id {task.id} was not found",
        "success": False,
    }, 404

    
    
    
    
    
    
