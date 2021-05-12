from tests.test_wave_01 import test_create_task_must_contain_description
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
                'id': task.task_id,
                'title': task.title,
                'description': task.description,
                'is_complete': task.completed_at != None
            })
        return jsonify(task_response)
    elif request.method == 'POST':
        request_body = request.get_json()
        if "title" not in request_body:
            return {
                "details": "Invalid data"
            }, 400
        elif "description" not in request_body:
            return {
                "details": "Invalid data"
            }, 400
        elif "is complete" not in request_body:
            return {
                "details": "Invalid data"
            }, 400

        new_task = Task(
            title = request_body['title'],
            description = request_body['description'], 
        )
        db.session.add(new_task)
        db.session.commit()
        return{
            'task':{
                'id': new_task.task_id,
                'title': new_task.title,
                'description': new_task.description,
                'is_complete': new_task.completed_at != None
            }      
        },201


@task_list_bp.route('/<task_id>', methods=['GET','PUT', 'DELETE'])
def handle_task(task_id):  # same name as parameter route
    task = Task.query.get(task_id)
    if not task:
        return "", 404

    if request.method == 'GET':
        return({
            'task': task.serialize()
        })
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return({
            "details": f'Task {task_id} "{task.title}" successfully deleted' 
        },200)
        

    elif request.method =='PUT':
        request_body = request.get_json()
        if 'title' in request_body:
            task.title = request_body['title']
        if 'description' in request_body:
            task.description = request_body['description']
        if 'completed_at' in request_body:
            task.completed = request_body['completed_at']
        db.session.commit()
        return({
            'task': task.serialize()
        },200)
        

    



