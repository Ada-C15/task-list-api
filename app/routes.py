from app import db
from .models.task import Task
from flask import request, Blueprint, make_response, jsonify


task_bp = Blueprint("task", __name__, url_prefix="/tasks")

#endpoint for new task entry post method 
@task_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()
    #checks to see if 'title' is found as a key in request_body
    if 'title' not in request_body:
        return make_response(jsonify({"details":"Invalid data"}), 400)
    if 'description' not in request_body:
        return make_response(jsonify({"details":"Invalid data"}), 400)
    if 'completed_at' not in request_body:
        return make_response(jsonify({"details":"Invalid data"}), 400)
    
    new_task = Task(title = request_body["title"], description = request_body["description"],completed_at = request_body['completed_at'])
    
    db.session.add(new_task)
    db.session.commit()
        
    return jsonify({
    "task": {
    "id": new_task.task_id,
    "title": new_task.title,
    "description": new_task.description,
    "is_complete": False
  }}), 201



#endpoint for getting tasks
@task_bp.route("", methods=["GET"])
def tasks():
    tasks = Task.query.all()
    request.method == "GET"
    task_response = []
    for task in tasks:
    #using to_json helper function 
        task_response.append(task.to_json())
    return jsonify(task_response), 200


#endpoint to get response body by task_id
@task_bp.route("/<task_id>", methods=["GET","PUT","DELETE"])
def task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return '',404
   
    if request.method == "GET":
        return jsonify(task=task.to_json()), 200
   
    
    if request.method =='PUT':
        request_body = request.get_json()
        #assigning edited values to task
        task.title = request_body['title']
        task.description = request_body['description']
        task.completed_at = request_body['completed_at']
        db.session.commit()
        return jsonify(task=task.to_json()), 200

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify(details=f'Task {task.task_id} "{task.title}" successfully deleted'),200







