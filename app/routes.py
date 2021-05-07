import requests
from app import db
from flask import request, Blueprint, make_response, jsonify
from app.models.task import Task
from sqlalchemy import desc, asc
from dotenv import load_dotenv
import os



load_dotenv()
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def slack_message(message):
    path = 'https://slack.com/api/chat.postMessage'
    query_params = {
        "channel": "bot-testing",
        "text": message
    }
    headers = {
        "Authorization": f'{os.environ.get("SLACK_API_KEY")}'
    }
    message = requests.post(path, params=query_params, headers=headers)
    return message.json()

@tasks_bp.route("", methods = ["GET", "POST"])
def handle_tasks():
    tasks_response = []
    if request.method == "GET":
        order = request.args.get("sort")
        if order == "asc":
            tasks_query = Task.query.order_by(Task.title)
        else:
            tasks_query = Task.query.order_by(Task.title.desc())
        for task in tasks_query:
            tasks_response.append(task.build_dict())
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body.keys() or "description" not in request_body.keys() or "completed_at" not in request_body.keys():
            return make_response({"details": "Invalid data"}, 400)
        
        new_task = Task(
            title=request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"],
        )
        db.session.add(new_task)
        db.session.commit()

        return {"task":new_task.build_dict()}, 201

@tasks_bp.route("/<task_id>", methods = ["GET", "PUT", "DELETE", "PATCH"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    if request.method == "GET":
        return make_response(jsonify({"task":task.build_dict()}))
    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return make_response(jsonify({"task":task.build_dict()}))
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}
    
@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        slack_message(f"Someone just completed {task.title}.")
        if not bool(task.completed_at):
            task.completed_at = True
        return {"task": task.build_dict()}, 200
    else:
        return jsonify(None), 404


@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        if bool(task.completed_at):
            task.completed_at = None
        return jsonify({"task": task.build_dict()}), 200
    else:
        return jsonify(None), 404




      
