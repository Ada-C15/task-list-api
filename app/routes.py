import requests
from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import desc
from datetime import date
from app import db
from app.models.task import Task
from app.models.goal import Goal
from dotenv import load_dotenv
import os

load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


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
        tasks_response.append(task.as_dict())
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

    return make_response(jsonify(task=task.as_dict()), 201)


@tasks_bp.route("/<int:task_id>", methods=["GET"], strict_slashes=False)
def get_task_by_id(task_id):
    """
    Returns a response with the task with given id as body and a 200 code
    when the task is found
    Returns a 404 with no response body in case the task is not found
    """
    task = Task.query.get(task_id)
    if task:
        return jsonify(task=task.as_dict())

    return make_response(jsonify(None), 404)


@tasks_bp.route("/<int:task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    """
    Deletes the task with a given id and returns a 200 response with a success 
    message
    Returns a 404 with no response body in case the task is not found
    """
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return make_response(jsonify(details=f"Task {task.task_id} \"{task.title}\" successfully deleted"), 200)
    return make_response(jsonify(None), 404)


@tasks_bp.route("/<int:task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    """
    Performs the update action and returns a 200 response with the newly updated task

    If any of the expected field is missing in the post request body, it returns
    a 400 response indicating invalid data

    Returns a 404 with no response body in case the task is not found
    """
    task = Task.query.get(task_id)
    if task:
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
        return make_response(jsonify(task=task.as_dict()), 200)
    return make_response(jsonify(None), 404)


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

        return make_response(jsonify(task=task.as_dict()), 200)
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
        return make_response(jsonify(task=task.as_dict()), 200)
    return make_response(jsonify(None), 404)


@goals_bp.route("", methods=["GET"], strict_slashes=False)
def list_all_goals():
    """
    Returns a 200 response with a list of all goals currently
    in the database as the response body
    Optional query arguments:
     * sort = asc or desc
    """

    query_param_value = request.args.get("sort")
    if query_param_value == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
    elif query_param_value == "asc":
        goals = Goal.query.order_by(Goal.title).all()
    else:
        goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.as_dict())
    return jsonify(goals_response)


@goals_bp.route("", methods=["POST"], strict_slashes=False)
def post_goal():
    """
    Returns a 201 response with a confirmation message as its body in case of
    a successful post

    If any of the expected field is missing in the post request body, it returns
    a 400 response indicating invalid data
    """
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    goal = Goal(title=request_body["title"])

    db.session.add(goal)
    db.session.commit()

    return make_response(jsonify(goal=goal.as_dict()), 201)


@goals_bp.route("/<int:goal_id>", methods=["GET"], strict_slashes=False)
def get_goal_by_id(goal_id):
    """
    Returns a response with the goal with given id as body and a 200 code
    when the goal is found
    Returns a 404 with no response body in case the goal is not found
    """
    goal = Goal.query.get(goal_id)
    if goal:
        return jsonify(goal=goal.as_dict())

    return make_response(jsonify(None), 404)


@goals_bp.route("/<int:goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):
    """
    Deletes the goal with a given id and returns a 200 response with a success 
    message
    Returns a 404 with no response body in case the goal is not found
    """
    goal = Goal.query.get(goal_id)
    if goal:
        db.session.delete(goal)
        db.session.commit()
        return make_response(jsonify(details=f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"), 200)
    return make_response(jsonify(None), 404)


@goals_bp.route("/<int:goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):
    """
    Performs the update action and returns a 200 response with the newly updated goal

    If any of the expected field is missing in the post request body, it returns
    a 400 response indicating invalid data

    Returns a 404 with no response body in case the goal is not found
    """
    goal = Goal.query.get(goal_id)
    if goal:
        request_body = request.get_json()

        if "title" not in request_body:
            return make_response({"details": "Invalid data"}, 400)

        goal.title = request_body["title"]
        db.session.commit()
        return make_response(jsonify(goal=goal.as_dict()), 200)
    return make_response(jsonify(None), 404)


@goals_bp.route("<int:goal_id>/tasks", methods=["POST"], strict_slashes=False)
def add_tasks_to_goal(goal_id):
    """
    Returns a 200 response with a confirmation message as its body in case of
    a successful post

    If any of the expected field is missing in the post request body, it returns
    a 400 response indicating invalid data
    """
    goal = Goal.query.get(goal_id)
    if goal:
        request_body = request.get_json()

        if "task_ids" not in request_body:
            return make_response({"details": "Invalid data"}, 400)

        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal_id

        db.session.commit()

        return make_response(jsonify(task_ids=request_body["task_ids"], id=goal_id), 200)
    return make_response(jsonify(None), 404)


@goals_bp.route("<int:goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_tasks_in_goal(goal_id):
    """
    Returns a 200 response with the goal and a list of tasks associated with it

    If the goal is not found returns a 404 response
    """
    goal = Goal.query.get(goal_id)
    if goal:
        goal_dict = goal.as_dict()
        goal_dict["tasks"] = []
        for task in goal.tasks:
            goal_dict["tasks"].append(task.as_dict())

        return make_response(jsonify(goal_dict), 200)
    return make_response(jsonify(None), 404)