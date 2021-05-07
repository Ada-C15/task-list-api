from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import asc, desc
from app import db 
from app.models.task import Task
from datetime import datetime
import requests
import os


tasks_bp = Blueprint(
    "tasks",
    __name__, 
    url_prefix="/tasks"
)

# create a new task 
@tasks_bp.route("", methods=["POST"])
def add_new_task():
    request_body = request.get_json()
    try:
        request_body["title"] 
        request_body["description"] 
        request_body["completed_at"] 
    except: 
        return make_response(jsonify({
        "details": "Invalid data"
        }),400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_json()}, 201)

# get all tasks asc, desc, unsorted
@tasks_bp.route("", methods=["GET"])
def list_all_tasks(): 
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc("title"))
    elif sort_query == "desc": 
        tasks = Task.query.order_by(desc("title"))
    else: 
        tasks = Task.query.all()
        # matt asked in order to google 
        # find out what type of data tasks is so i can look at methods for that in documentation 
    tasks_response = []
    for task in tasks: 
        tasks_response.append(task.to_json())
    return jsonify(tasks_response)

# get one task by id 
@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = Task.query.get(task_id)
    if task: 
        task_response = {"task": task.to_json()}
        return task_response 
    
    return make_response("Task not found. Less to do then :)", 404)

# update one task by id 
@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task_by_id(task_id): 
    task = Task.query.get(task_id)
    if task: 
        request_body = request.get_json()

        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]

        db.session.commit()

        return make_response({"task": task.to_json()})

    return make_response("", 404)

# mark compelte on an incompleted task
@tasks_bp.route("/<int:task_id>/<complete_status>", methods=["PATCH"])
# status is a route paramter
# how to know if it a query param
def patch_task_by_id(task_id, complete_status): 
    task = Task.query.get(task_id)
    PATH = "https://slack.com/api/chat.postMessage"

    # status = request.args.get("complete_status")
    # dont need bc complete_status is a route parameter 
    if task is None: 
        return make_response("", 404)

    if complete_status == "mark_complete": 
        date = datetime.today()
        task.completed_at = date
        query_params = {
            "channel": "task-notifications",
            "text": "u done did it"
        }
        
        headers = {
            "Authorization" : f"Bearer {os.getenv('SLACK_TOKEN')}"
        }
        response = requests.post(PATH, params=query_params, headers=headers)

    else:
        task.completed_at = None

    db.session.commit()

    return make_response({"task": task.to_json()})



# delete one task by id 
@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task_by_id(task_id):
    task = Task.query.get(task_id)
    if task: 
        db.session.delete(task)
        db.session.commit()
        return make_response({
        "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    })
    
    return make_response("", 404)

