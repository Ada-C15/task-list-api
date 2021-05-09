from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, make_response, request, jsonify, request
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():     
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return {
                "details": "Invalid data"
            }, 400
    
        new_task = Task(title=request_body['title'], 
                        description=request_body['description'],
                        completed_at=request_body['completed_at'])
        
        db.session.add(new_task)
        db.session.commit()
        response_body = {
            "task": new_task.resp_json()
        }
        return jsonify(response_body), 201

    elif request.method == "GET":
        sorting_tasks = request.args.get("sort")
        
        tasks = Task.query.all()
        tasks_response = []

        if sorting_tasks == "asc":
            asc_order = Task.query.order_by(Task.title.asc())
            new_order = []
        
            for task in asc_order:
               new_order.append(task.resp_json())
            return jsonify(new_order), 200

        elif sorting_tasks == "desc":
            desc_order = Task.query.order_by(Task.title.desc())
            new_order = []
        
            for task in desc_order:
               new_order.append(task.resp_json())
            return jsonify(new_order), 200


        for task in tasks:
            tasks_response.append(task.resp_json())
            
        print(request.view_args)

        return jsonify(tasks_response), 200




    
        
@tasks_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def handle_task(id):
    task = Task.query.get(id)

    if task is None: 
        return  make_response("", 404)
    if request.method == "GET":
        response_body = {
                "task": task.resp_json()
            }
        return jsonify(response_body), 200

    elif request.method == "PUT":

        request_body = request.get_json()
    
        task.title=request_body['title'], 
        task.description=request_body['description'],
        task.completed_at=request_body['completed_at']
        
        db.session.add(task)
        db.session.commit()

        response_body = {
                "task": task.resp_json()
            }
        return jsonify(response_body), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        
        return {
            "details": f"Task {task.id} \"{task.title}\" successfully deleted"
        }, 200

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])

def task_completed(id):
    task = Task.query.get(id)

    if task is None:
        return make_response("", 404)
    
    task.completed_at = datetime.now()
    db.session.commit()

    response_body = {
            "task": task.resp_json()
        }
    return jsonify(response_body), 200

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])

def task_incomplete(id):
    task = Task.query.get(id)

    if task is None:
        return make_response("", 404)
    
    task.completed_at = None
    db.session.commit()

    response_body = {
            "task": task.resp_json()
        }
    return jsonify(response_body), 200