from flask import Blueprint
from app.models.task import Task
from app import db
from flask import request, Blueprint, make_response, Response, jsonify
from datetime import date
import requests
from secrets import slack_token
# slack_token = os.environ.get("slack_token")

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET", "POST"])
def handle_tasks(): 
    if request.method == "GET":

        tasks = Task.query.all()
        tasks_response = []

        for task in tasks:
            if task.completed_at == None:
                completed_at = False
            else:
                completed_at = True

            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": completed_at
            })

        # sort before return
        sort = request.args.get("sort")
        if sort == "asc":
            # def test_get_tasks_sorted_asc
            tasks_response = sorted(tasks_response, key=lambda x: x["title"])
        elif sort == "desc":
            # def test_get_tasks_sorted_desc(client, three_tasks):
            tasks_response = sorted(
                tasks_response, key=lambda x: x["title"], reverse=True)
        return jsonify(tasks_response)

    elif request.method == "POST":  # CRUD CREATE
        # check for request body title and description, plus ensure both are strings
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return {
                "details": f"Invalid data"
            }, 400

        completed_at = request_body["completed_at"]

        task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"]
        )

        db.session.add(task)
        db.session.commit()

        if task.completed_at == None:
            completed_at = False
        else:
            completed_at = True
        return {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": completed_at
            }
        }, 201

# getting 1 task
@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response(f"Task {task_id} not found", 404)

    if request.method == "GET":
        if task.completed_at == None:
            completed_at = False
        else:
            completed_at=True
        return {"task":task.get_json()}

    elif request.method == "PUT":
        form_data = request.get_json()

        #update_task = Task.
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        if task.completed_at == None:
            completed_at = False
        else:
            completed_at = True
        return {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": completed_at
            }
        }

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        if task.completed_at == None:
            completed_at = False
        else:
            completed_at = True
        return {
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return "",404

    task.completed_at = date.today()  # todays date

    db.session.commit()

    r = requests.post(f"https://slack.com/api/chat.postMessage?channel=task-notifications&text=Someone just completed the task {task.title}", headers={"Authorization":slack_token})

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
        }
    }

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    
    if task == None:
        return "",404

    task.completed_at = None

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

