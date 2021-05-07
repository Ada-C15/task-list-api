from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime
from app.slack import slack_message
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET"])
def handle_tasks_get():
    """
    - Get all saved tasks.
    - Get all saved tasks filtered by title in asc and desc order.
    """
    title_query = request.args.get("sort")

    if title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_one_task_get(task_id):
    """
    Get specific tasks by id.
    """
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    if task:
        return ({"task": task.to_dict()}, 200)


@tasks_bp.route("", methods=["POST"])
def handle_tasks_post():
    """
    Create a Task.
    """
    request_body = request.get_json()

    # task to create must contain: - title, - description, - completed_at,
    # otherwise 404 + details
    if ("title" not in request_body.keys()) or (
        "description" not in request_body.keys()) \
            or ("completed_at" not in request_body.keys()):
        return make_response({
            "details": "Invalid data"
        }, 400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"]
                    )

    db.session.add(new_task)
    db.session.commit()

    # todo: retrieve committed task to the db, not the one with id 1
    retrieve_task = Task.query.get(new_task.task_id)

    return {"task": retrieve_task.to_dict()}, 201


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def handle_one_task_delete(task_id):
    """
    Delete task with specific id.
    """
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    if task:
        db.session.delete(task)
        db.session.commit()
        return ({
            "details": f'Task {task.task_id} "{task.title}" successfully deleted'
        }, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def handle_one_task_update(task_id):
    """
    Update task with specific id.
    """
    task = Task.query.get(task_id)

    if task is None:  # task not found
        return jsonify(None), 404

    data_to_update_with = request.get_json()
    task.title = data_to_update_with["title"]
    task.description = data_to_update_with["description"]
    task.completed_at = data_to_update_with["completed_at"]

    db.session.commit()

    retrieve_task = Task.query.get(task.task_id)

    return ({"task": retrieve_task.to_dict()}, 200)


def slack_send_message():
    path = "https://slack.com/api/chat.postMessage"
    auth = f'Bearer {os.environ.get("SLACK_BOT_TOKEN")}'

    print(auth)

    query_params = {
        "channel": "task-notifications",
        "text": f"Hello! Current date: {datetime.now()}"
    }

    headers = {
        "Authorization": auth
    }

    slask_request = requests.post(path,
                                  params=query_params,
                                  headers=headers)
    print(slask_request)
    # print(slask_request.json())
    return slask_request


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def handle_one_task_complete_patch(task_id):
    """
    Mark Complete on an Incompleted Task
    """

    if True:
        slack_message()

    task = Task.query.get(task_id)

    if task is None:  # task not found
        return jsonify(None), 404

    task.completed_at = datetime.utcnow()
    db.session.commit()

    retrieve_task = Task.query.get(task.task_id)

    return ({"task": retrieve_task.to_dict()}, 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def handle_one_task_incomplete_patch(task_id):
    """
    Mark InComplete on an Completed Task
    """
    task = Task.query.get(task_id)

    if task is None:  # task not found
        return jsonify(None), 404

    task.completed_at = None
    db.session.commit()

    retrieve_task = Task.query.get(task.task_id)

    return ({"task": retrieve_task.to_dict()}, 200)
