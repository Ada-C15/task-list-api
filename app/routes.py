from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
import datetime
import os
import requests

'''
Get All Tasks and Post A Task
'''
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])

def handle_tasks():
    if request.method == "GET":
        query_param_value = request.args.get("sort")
        if query_param_value == "asc":
            tasks = Task.query.order_by(Task.title.asc())
            # tasks = Task.query.filter_by(title=title_query)
        elif query_param_value == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
            })
            # tasks_response.append(task.to_dict())
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        
        # Invalid task if missing title, description, or completed_at     
        if "completed_at" not in request_body or "description" not in request_body or "title" not in request_body:
            return jsonify(details="Invalid data"), 400
        else:
            new_task =  Task(
                title = request_body["title"],
                description = request_body["description"],
                completed_at = request_body["completed_at"])
        
            # add this model to the database and commit the changes
            db.session.add(new_task)
            db.session.commit()

            return jsonify(task= {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": True if new_task.completed_at is not None else False
            }), 201
            # return new_task.to_dict(), 201


'''
Get One Task, Update One Task, Delete One Task
'''
@tasks_bp.route("/<task_id>", methods=["GET","PUT","DELETE"], strict_slashes=False)
def handle_single_task(task_id):

    # Find the task with the given id
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
        # return make_response(jsonify(None), 404)

    if request.method == "GET": 
        return make_response(jsonify(task= {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": True if task.completed_at is not None else False
        }), 200)
        # return jsonify(task=task.to_dict())
    

    elif request.method == "PUT":
        new_data = request.get_json()

        task.title = new_data["title"]
        task.description = new_data["description"]
        task.completed_at = new_data["completed_at"]

        db.session.commit()

        return jsonify(task= {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at is not None else False
        }), 200

        # return make_response(jsonify(task=task.to_dict()), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()

        return make_response(jsonify(details=f"Task {task.id} \"{task.title}\" successfully deleted"), 200)

'''
Wave 03: Mark a tast complete or incomplete
'''
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    if request.method == "PATCH":

        task.completed_at = datetime.datetime.now()

        db.session.commit()

        send_slack(task)

        return jsonify(task= {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            # "is_complete": True if task.completed_at is not None else False
            "is_complete": bool(task.completed_at)
        }), 200

def send_slack(task):

        text = f"Someone just completed the task {task.title}"
        path = f"https://slack.com/api/chat.postMessage?channel=task-notifications&text={text}"
        token = os.environ.get("API_KEY")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.request("POST", path, headers=headers)
        
        return response


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    if request.method == "PATCH":

        task.completed_at = None

        db.session.commit()

        return jsonify(task= {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }), 200

    

