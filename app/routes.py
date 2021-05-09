from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify

task_bp = Blueprint("task", __name__, url_prefix='/tasks')


# @task_bp.route("", methods=["GET"])
# def handle_tasks():
#         #return full list of tasks
#     tasks = Task.query.all()
#     task_response_body = []
#     for task in tasks:
#         task_response_body.append({
#             'id': task.id,
#             'title': task.title,
#             'description': task.description,
#             'is_complete': task.is_complete
#         })
#     return jsonify(task_response_body), 200

# @task_bp.route('/<task_id>', methods=['GET'])
# def handle_task(task_id):  # same name as parameter route
#     task = Task.query.get(task_id)
#     if not task:
#         return "", 404
#     return jsonify({
#         "task":{
#             "id": task.id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": task.is_complete
#         }      
#     }), 201
    

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

