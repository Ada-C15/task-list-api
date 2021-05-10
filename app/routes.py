from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def post_to_slack(text, request_method):
    """
    Posts a message to Slack channel
    text is the string to be posted
    request_method is the type of request, e.g. requests.patch
    """
    headers = {"Authorization": os.environ.get("SLACK_KEY")}
    data = {
        "channel": "C021GPYFGKT",
        "text": text
    }

    request_method('https://slack.com/api/chat.postMessage',
    headers=headers, data=data)

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    """
    Gets all tasks, with option of querying by ascending or descending order
    Posts new task
    """
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title)
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.all()

        tasks_response = [] # Can I use to_json() in a loop like this?
        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
            })
        return jsonify(tasks_response) # why does this need to use jsonify? because it's a list?

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body\
            or "completed_at" not in request_body:
            return ({
                "details": "Invalid data"
            }, 400)
        else:
            new_task = Task(title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"])

            db.session.add(new_task)
            db.session.commit()

            return new_task.to_json(), 201

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    """
    Gets task by task_id
    Updates specific task information
    Deletes task by task_id
    """
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        return task.to_json()
    elif request.method == "PUT":
        form_data = request.get_json()

        #task.from_json(form_data)

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return task.to_json()
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {
            "details": (f'Task {task.task_id} "{task.title}" successfully deleted')
        }

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    """
    Marks task as complete and posts notification message to Slack channel
    """
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    task.completed_at = datetime.utcnow()

    post_to_slack(f"Someone just completed the task {task.title}", requests.patch)

    return task.to_json()

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    """
    Marks task as incomplete
    """
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    task.completed_at = None

    return task.to_json()

@goals_bp.route("", methods=["POST", "GET"])
def handle_goals():
    """
    Gets all goals
    Posts new goal
    """

    if request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body:
            return ({
            "details": "Invalid data"
            }, 400)

        new_goal = Goal(
            title=request_body["title"])

        db.session.add(new_goal)
        db.session.commit()

        return (new_goal.to_json(), 201)
    elif request.method == "GET":
        goals = Goal.query.all()

        goals_response = []
        for goal in goals:
            goals_response.append({
                "id": goal.goal_id,
                "title": goal.title,
            })
        return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(goal_id):
    """
    Gets goal by goal_id
    Updates specific goal information
    Deletes goal by goal_id
    """
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)

    if request.method == "GET":
        return goal.to_json()
    elif request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data["title"]

        db.session.commit()

        return goal.to_json()
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return {
            "details": (f'Goal {goal.goal_id} "{goal.title}" successfully deleted')
        }

@goals_bp.route("/<goal_id>/tasks", methods=["GET", "POST"])
def handle_goals_tasks(goal_id):
    """
    Gets list of tasks associated with goal_id
    Creates new relationship between goal and list of tasks
    """
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    if request.method == "GET":
        tasks = Task.query.filter_by(goal_id=goal.goal_id)

        tasks_response = []
        for task in tasks: # Can I use to_json() in a loop like this?
            tasks_dict = {
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
            }
            tasks_response.append(tasks_dict)

        return {
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": tasks_response
        }

    elif request.method == "POST":
        request_body = request.get_json()

        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal.goal_id

        db.session.commit()

        return {
            "id": goal.goal_id,
            "task_ids": request_body["task_ids"]
        }
