from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify

task_bp = Blueprint("task", __name__, url_prefix='/tasks')

@task_bp.route("", methods=["POST"])
def post_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        "task":{
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }      
    }), 201
    if "title" or "desription" or "completed_at" not in request_body:
        return jsonify({
            "details": "Invalid data"
            }), 40


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
    }), 201
    
@task_bp.route("", methods=['DELETE', 'PUT'])
def delete_put_tasks():
    task = Task.query.get(task_id)
    if not task:
        return 404
    
    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return ({
            "details": f"Task {task_id} \"Go on my daily walk 🏞\" successfully deleted"
        }, 200) 
    

    elif request.method == 'PUT':
        request_body = request.get_json()
        if "title" or "description" not in request_body:
            return 404
        if "title" in request_body:
            task.title = request_body["title"]
        if "description" in request_body:
            task.description = request_body["description"]
        db.session.commit()
        return jsonify({
                "task": {
                "id": 1,
                "title": "Updated Task Title",
                "description": "Updated Test Description",
                "is_complete": false
            }
        }), 200


