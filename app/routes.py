from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"], strict_slashes= False)
def deal_tasks():
    title = None
    description = None
    completed_at = None
    if request.method == "GET":
        tasks = Task.query.order_by(Task.title).all()
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.to_json())
        return jsonify(tasks_response)
        
    elif request.method == "POST":
        request_body = request.get_json()
       
        if "title" in request_body and "description" in request_body and "completed_at" in request_body:
            new_task = Task(title = request_body["title"],
                        description = request_body["description"],
                        completed_at = request_body["completed_at"])
                        
            db.session.add(new_task)
            db.session.commit()
            return make_response({"task": new_task.to_json()}, 201)
        else:
            return jsonify({"details": "Invalid data"}), 400


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes= False)
def get_task_by_id(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None), 404
    else:
        return make_response({"task": task.to_json()}, 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes= False)
def delete_task(task_id):
    print("in delete task")
    task = Task.query.get(task_id) #what is .query.get returning
    if task is None:
        return jsonify(None), 404
    else:
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes= False)
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None), 404
    
    form_data = request.get_json()

    task.title = form_data["title"]
    task.description = form_data["description"]
    task.completed_at = form_data["completed_at"]
    
    db.session.commit()
    
    return jsonify({"task":task.to_json()}), 200
  






