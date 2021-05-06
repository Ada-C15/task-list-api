import requests
from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import desc
from datetime import date
from app import db
from app.models.task import Task
from dotenv import load_dotenv
import os

load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def list_all_tasks():
    """
    Returns a 200 response with a list of all tasks currently
    in the database as the response body
    Optional query arguments:
     * sort = asc or desc
    """

    query_param_value = request.args.get("sort")
    if query_param_value == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif query_param_value == "asc":
        tasks = Task.query.order_by(Task.title).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.task_view())
    return jsonify(tasks_response)


@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def post_task():
    """
    Returns a 201 response with a confirmation message as its body in case of
    a successful post

    If any of the expected field is missing in the post request body, it returns
    a 400 response indicating invalid data
    """
    request_body = request.get_json()

    if ("completed_at" not in request_body
        or "description" not in request_body
            or "completed_at" not in request_body
            or "title" not in request_body):
        return make_response({"details": "Invalid data"}, 400)

    task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"])

    db.session.add(task)
    db.session.commit()

    return make_response(jsonify({"task": task.task_view()}), 201)


@tasks_bp.route("/<int:task_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def handle_task_by_id(task_id):
    """
    GET: Returns a response with the task with given id as body and a 200 code
    when the task is found
    PUT: tries to update the task and returns a response with the updated task 
    and a 200 code
    DELETE: tries to delete the task and returns a 200 response with a success 
    message
    Returns a 404 with no response body in case the task is not found
    """
    task = Task.query.get(task_id)
    if task:
        task_response = {"task": task.task_view()}
        if request.method == "GET":
            return jsonify(task_response)
        elif request.method == "DELETE":
            return delete_task(task)
        elif request.method == "PUT":
            return update_task(task)
    return make_response(jsonify(None), 404)


def delete_task(task):
    """
    Helper function that performs the delete action and returns a 200 response
    with a confirmation message
    """
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}), 200)


def update_task(task):
    """
    Helper function that performs the update action and returns a 200 response
    with the newly updated task
    """
    request_body = request.get_json()

    if ("completed_at" not in request_body
        or "description" not in request_body
            or "completed_at" not in request_body
            or "title" not in request_body):
        return make_response({"details": "Invalid data"}, 400)

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]
    db.session.commit()
    return make_response(jsonify({"task": task.task_view()}), 200)


@tasks_bp.route("/<int:task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_task_complete(task_id):
    """
    Changes the task.completed_at value to todays date and returns a 200 response
    with the updated task and calls the send_task_notification funtion
    Returns a 404 with no response body in case the task is not found
    """
    task = Task.query.get(task_id)
    if task:
        task.completed_at = date.today()
        db.session.commit()

        send_slack_task_notification(task)

        return make_response(jsonify({"task": task.task_view()}), 200)
    return make_response(jsonify(None), 404)


def send_slack_task_notification(task):
    """
    Sends a request to a slack bot to post the
    "Someone just completed the task <TASK_TITLE>" to the task-notifications channel
    in the configured slack workspace
    """
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    text = f"Someone just completed the task {task.title}"
    url = f"https://slack.com/api/chat.postMessage?channel=task-notifications&text={text}"

    payload = ""

    headers = {
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
    }

    return requests.request("POST", url, headers=headers, data=payload)


@tasks_bp.route("/<int:task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_task_incomplete(task_id):
    """
    Changes the task.completed_at value to None and returns a 200 response
    with the updated task
    Returns a 404 with no response body in case the task is not found
    """
    task = Task.query.get(task_id)
    if task:
        task.completed_at = None
        db.session.commit()
        return make_response(jsonify({"task": task.task_view()}), 200)
    return make_response(jsonify(None), 404)
