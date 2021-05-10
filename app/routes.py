from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify
from datetime import datetime
import requests
from app import slack_key

task_list_bp = Blueprint("task_list", __name__, url_prefix = "/tasks")

@task_list_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    attributes = ["title", "description", "completed_at"]

    for attribute in attributes:
        if attribute not in request_body:

            return make_response({"details": "Invalid data"}), 400

    new_task = Task(title = request_body["title"],
                description = request_body["description"],
                completed_at = request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json()}), 201


@task_list_bp.route("", methods = ["GET"]) 
def get_all_tasks():
    # tasks = Task.query.all()
    sort_method = request.args.get("sort")
    if sort_method == "asc":
        tasks = Task.query.order_by(Task.title.asc())
        # SELECT * FROM task ORDER BY title ASC
    elif sort_method == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    task_response = []
    for task in tasks:
        task_response.append(task.to_json())

    return jsonify(task_response), 200


@task_list_bp.route("/<task_id>", methods = ["GET", "DELETE", "PUT"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return (f"Task not found", 404)

    if request.method == "GET":
        return make_response({"task": task.to_json()}), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200

    if request.method == "PUT":
        request_body = request.get_json()

        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]

        db.session.commit()

        return jsonify({"task": task.to_json()}), 200


@task_list_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
# url = 'https://www.w3schools.com/python/demopage.php'
# myobj = {'somekey': 'somevalue'}

# x = requests.post(url, data = myobj)
    
    if task == None:
        return make_response(), 404
    
    task.completed_at = datetime.utcnow()
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    data = {
        "channel": "C020W6FPXQX",
        "text": (f"Someone just completed the task {task.title}")
        }
    headers = {
        "Authorization": f"Bearer {slack_key}"
        }
    x = requests.post(url, data = data, headers = headers)
    
    return jsonify({"task": task.to_json()}), 200

@task_list_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response(), 404

    task.completed_at = None
    db.session.commit()

    return jsonify({"task": task.to_json()}), 200