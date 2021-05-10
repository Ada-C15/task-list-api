from app import db
from app.models.task import Task
from flask import request
from flask import request, Blueprint, make_response
from flask import jsonify
from datetime import datetime 
from sqlalchemy import asc, desc
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#localhost:9000/tasks/2
@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_single_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    complete = task.completed_at_helper()  # Helper function to return boolean

    if request.method == "GET":
        return jsonify({"task": task.json_object()}), 200

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.is_complete = form_data["completed_at"] 

        db.session.commit()
        return jsonify({"task": task.json_object()}),200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200


@task_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        
        request_value = request.args.get("sort") 
        
        if request_value == None:
            tasks = Task.query.all()

        if request_value == "asc": # checking if there is a sort arg with the value of asc.
            tasks = Task.query.order_by(Task.title.asc()) #Task is the the model and query is a class method 
        
        
        if request_value == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        task_response = []

        for task in tasks:
            # using jsonobject helper to create a dictionary with id, title, description, isComplete
            task_response.append(task.json_object())
        
        return jsonify(task_response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "completed_at" not in request_body or "description" not in request_body or "title" not in request_body:
            return jsonify({
                "details": "Invalid data"
            }), 400

        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()
        # called my new_task.completed_at_helper.
        # created a new task and changed my task objet into JSON
        # using jsonobject helper to create a dictionary with id, title, description, isComplete
        return jsonify({"task": new_task.json_object()}), 201

        db.session.add(new_task)
        db.session.commit()
    
#PATCH localhost:9000/tasks/1/mark_complete
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):
    # If POSTMAN (request)searches for a patch path 
    if request.method == "PATCH":
        #query is seaching TASK (ID, TITLE, DESCRIPTION, AND COMPLEATED_AT) and "get" getting the task_id
        task = Task.query.get(task_id)
        # If the task is NONE return the not found 404 code 
        if task is None:
            return jsonify(None), 404
        # If None is found than my code searches for what id is being mark_compleated and with my compleated_at_helper() marking complete turn/
        # into a true statement which then timestamps the date and time completed.
        task.completed_at = datetime.now()
        #jsonify my object and "task"(STR) json_object is the jsonifyed id, title, description, and compleated_at function 
        return jsonify({"task": task.json_object()}),200 # 200 ok code 

#PATCH localhost:9000/tasks/2/mark_incomplete(is saying this id should be marked as complete)
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):
    
    if request.method == "PATCH":
        #query is seaching TASK (ID, TITLE, DESCRIPTION, AND COMPLEATED_AT) and "get" getting the task_id
        task = Task.query.get(task_id)
        # If the task is NONE return the not found 404 code 
        if task is None:
            return jsonify(None), 404
        
        task.completed_at = None
        
        return jsonify({"task": task.json_object()}),200
    

# post man testing eviroment
#API request using url request can i find route that matches




