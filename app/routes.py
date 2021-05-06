from flask import Blueprint, request, make_response, jsonify
from app import db 
from app.models.task import Task

tasks_bp = Blueprint(
    "tasks",
    __name__, 
    url_prefix="/tasks"
)

# create a new task 
@tasks_bp.route("", methods=["POST"])
def add_new_task():
    request_body = request.get_json()
    try:
        request_body["title"] 
        request_body["description"] 
        request_body["completed_at"] 
    except: 
        return make_response(jsonify({
        "details": "Invalid data"
        }),400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_json()}, 201)

# get all tasks 
@tasks_bp.route("", methods=["GET"])
def list_all_tasks(): 
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks: 
        tasks_response.append(task.to_json())
    return jsonify(tasks_response)

# get one task by id 
@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = Task.query.get(task_id)
    if task: 
        task_response = {"task": task.to_json()}
        return task_response 
    
    return make_response("Task not found. Less to do then :)", 404)