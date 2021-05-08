from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response
from flask import jsonify
from sqlalchemy import asc, desc
import time
import datetime
import requests
from flask import current_app as app
import os 

path = "https://slack.com/api/chat.postMessage"

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def tasks():
    print(request)
    if request.method == "GET":  
        task_order = request.args.get("sort") 
        if task_order == None:
            tasks = Task.query.all() # Task is the model and query is a class method (query is like go get my info)
        elif task_order == "asc":
            tasks = Task.query.order_by(asc(Task.title))
        elif task_order == "desc":
            tasks = Task.query.order_by(desc(Task.title))

        tasks_response = []
        for task in tasks: 
        
            tasks_response.append(task.to_json())
            
                
        return jsonify(tasks_response)
    # using the "PUT" to add a new task
    else:
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)
            
        task = Task(title = request_body["title"],
                            description = request_body["description"],
                            completed_at = request_body["completed_at"])
        

        db.session.add(task)
        db.session.commit()

        return jsonify({"task": task.to_json()}),201
    
        # return make_response(jsonify({"task": task.to_jason()})),201 
    

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_task(task_id):
    # Try to find the task with the given id

    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        
        return jsonify({"task": task.to_json()}),200

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return jsonify({"task": task.to_json()})

    

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": (f"Task {task.task_id} \"{task.title}\" successfully deleted")})
    
    
    return {
        "message": f"Task with id {task_task_id} was not found",
        "success": False,
    }, 404




@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def task_complete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    elif task:
        task.completed_at = datetime.datetime.now()
    # if task mark a complete then send a message
        key = os.environ.get("AUTHORIZATION")

        query_params = {
                "text": f"Someone just completed the task {task.title}",
                "channel": "task-notifications"
                
            }

        query_headers = {
            "authorization": f"Bearer {key}"
        }
        response = requests.post(path, params=query_params, headers=query_headers )
        response_body = response.json()

        print(response)
        
        
        db.session.commit() 
        
        return jsonify({"task": task.to_json()}),200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def task_incomplete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    elif task:
        task.completed_at = None
        
        db.session.commit()
        
        return jsonify({"task": task.to_json()}),200


            


