from app import db
from .models.task import Task
from flask import Blueprint, request, make_response, jsonify


task_bp = Blueprint("task", __name__, url_prefix='/tasks')

@task_bp.route("", methods=["POST"])
def post_task():
    request_body = request.get_json()
    if "title" in request_body and "description" in request_body and "completed_at" in request_body:
        new_task = Task(title=request_body["title"],description=request_body["description"], 
                    completed_at=request_body["completed_at"])
    else:   
        return make_response({
            "details": "Invalid data"
        }), 400
    
    
    db.session.add(new_task)
    db.session.commit()
    
    
    return jsonify({"task": new_task.to_json()}), 201
    


@task_bp.route("", methods=["GET"])
def handle_tasks():
        #return full list of tasks
    tasks = Task.query.all()
    task_response_body = []
    for task in tasks:
        task_response_body.append({
            'id': task.task_id,
            'title': task.title,
            'description': task.description,
            'is_complete': task.is_complete
        })
    return jsonify(task_response_body), 200

@task_bp.route('/<task_id>', methods=['GET'])
def handle_task(task_id):  # same name as parameter route
    task = Task.query.get(task_id)
    if not task:
        return "", 404
    return jsonify({
        "task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }      
    }), 200
    
@task_bp.route("/<task_id>", methods=['DELETE', 'PUT'])
def delete_or_put_tasks(task_id):
    task = Task.query.get(task_id)
    if not task:
        return "", 404
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({
            "details": f"Task {task_id} \"Go on my daily walk 🏞\" successfully deleted"
            }), 200
        
    elif request.method == 'PUT':
        request_body = request.get_json()
    
        task.title = request_body["title"]
    
        task.description = request_body["description"]
        db.session.commit()
        return jsonify({"task": task.to_json()}), 200
        
        


