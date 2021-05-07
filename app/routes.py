from flask import Blueprint
from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify

task_list_bp = Blueprint("task_list", __name__, url_prefix='/tasks')
@task_list_bp.route('', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        #return full list of tasks
        tasks = Task.query.all()
        task_response = []
        for task in tasks:
            task_response.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'is_complete': task.is_complete
            })
        return jsonify(task_response)
    
@task_list_bp.route('/<task_id>', methods=['GET'])
def handle_task(task_id):  # same name as parameter route
    task = Task.query.get(task_id)
    if not task:
        return "", 404
    return({
        'task':{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'is_complete': task.is_complete
        }      
    })


