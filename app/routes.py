from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify


task_bp = Blueprint("task", __name__, url_prefix="/tasks")

#endpoint for new task entry post method 
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
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
    
        
    task_response = []
    for task in tasks:
        #using to_json helper function in tasks to retrun json format 
        task_response.append(task.to_json()
        )
    #     {
    #     "task_id": task.task_id,
    #     "title": task.title,
    #     "description": task.description,
    #     "completed_at": task.completed_at
    # }
    return jsonify(task_response), 200

# endpoint to get a cutomized response body by task_id
@task_bp.route("/<task_id>", methods=["GET"])
def task(task_id):
    task = Task.query.get(task_id)
    #task_dict = {'task': task}
    # return task.to_json(), 200
    return make_response({"task":task.to_json()}), 200

