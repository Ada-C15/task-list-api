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
    
    # grabbing sort query parameter and its value ex. sort=asc from the client request and storing it in local variable
    sort_titles = request.args.get('sort')
    # if sort query param is in the body request of the user, we need to now check what the value of sort parameter. If value is set to sort=asc then.... else if sort=desc do...
    #if sorts value == asc then ....
    task_response = []
    if sort_titles:
        if sort_titles == "asc":
            task_by_asc = Task.query.order_by(Task.title.asc())
            for task in task_by_asc:
                task_response.append(task.to_json())   
        
        if sort_titles == 'desc':
            task_by_desc = Task.query.order_by(Task.title.desc())
            for task in task_by_desc:
                task_response.append(task.to_json())
        
        return jsonify(task_response), 200
    
    else:
        tasks = Task.query.all()
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
        #assigning updated values to task
        task.title = request_body['title']
        task.description = request_body['description']
        task.completed_at = request_body['completed_at']
        db.session.commit()
        return jsonify(task=task.to_json()), 200

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify(details=f'Task {task.task_id} "{task.title}" successfully deleted'),200







