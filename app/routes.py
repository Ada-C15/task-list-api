from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, make_response, request, jsonify
from sqlalchemy import desc
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()

        try:
            new_task = Task(title=request_body['title'],
                            description=request_body['description'],
                            completed_at=request_body['completed_at'])
        except KeyError:
            return make_response({
                "details": "Invalid data"
            }, 400)

        db.session.add(new_task)
        db.session.commit()

        response = {
            "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": is_task_complete(new_task)
            }
        }

        return make_response(jsonify(response), 201)

    elif request.method == "GET":

        sort_query = request.args.get("sort")

        if sort_query == "asc":
            tasks = Task.query.order_by("title")
        elif sort_query == "desc":
            tasks = Task.query.order_by(desc("title"))
        else:
            tasks = Task.query.all()

        tasks_response = []

        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description":task.description,
                "is_complete": is_task_complete(task)
            })

        return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    if request.method == "GET":
    
        response = {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_task_complete(task),
            }
        }

        if task.goal_id:
            response['task']['goal_id'] = task.goal_id

        return response

    elif request.method == "PUT":

        request_body = request.get_json()

        task.title = request_body['title']
        task.description = request_body['description']
        task.completed_at = request_body['completed_at']

        db.session.commit()

        return {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_task_complete(task)
            }
        }

    elif request.method == "DELETE":

        db.session.delete(task)
        db.session.commit()

        return {
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    task.completed_at = None

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_task_complete(task)   # False
        }
    }


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    task.completed_at = datetime.now()

    post_to_slack(f"Someone just completed the task {task.title}")

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_task_complete(task)   # False
        }
    }

@goals_bp.route("", methods=['POST', 'GET'])
def handle_goals():
    if request.method == "POST":
        request_body = request.get_json()

        try:
            new_goal = Goal(title=request_body['title'])
        except KeyError:
            return make_response({
                "details": "Invalid data"
            }, 400)

        db.session.add(new_goal)
        db.session.commit()

        response = {
            "goal": {
                "id": new_goal.goal_id,
                "title": new_goal.title
            }
        }

        return make_response(jsonify(response), 201)

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
def handle_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    if request.method == "GET":
        return {
            "goal": {
                "id": goal.goal_id,
                "title": goal.title
            }
        }

    elif request.method == "PUT":
        request_body = request.get_json()

        goal.title = request_body["title"]

        db.session.commit()

        return {
            "goal": {
                "id": goal.goal_id,
                "title": goal.title
            }
        }

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()

        return {
            "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        }

@goals_bp.route("/<goal_id>/tasks", methods=["POST", "GET"])
def handle_tasks_for_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    if request.method == "POST":
        request_body = request.get_json()

        for task_id in request_body['task_ids']:
            task = Task.query.get(task_id)
            task.goal_id = int(goal_id)
            
        db.session.commit()

        return {
            "id": int(goal_id),
            "task_ids": request_body['task_ids']
        }

    elif request.method == "GET":
        associated_tasks = Task.query.filter_by(goal_id=int(goal_id))

        associated_tasks_info = []
        for task in associated_tasks:
            task_info = {
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_task_complete(task)
            }
            associated_tasks_info.append(task_info)

        response = {
            "id": int(goal_id),
            "title": goal.title,
            "tasks": associated_tasks_info
        }

        return response


# Helper functions
def is_task_complete(task):
    if not task.completed_at:
        return False
    return True

def post_to_slack(message):
    """
    Posts a given message to the task-notifications channel in my Task Manager Slack workspace.
    """
    path = "https://slack.com/api/chat.postMessage"

    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")

    auth_header = {
        "Authorization": f"Bearer {SLACK_API_KEY}"
    }

    query_params = {
        "channel": "task-notifications",
        "text": message
    }

    requests.post(path, params=query_params, headers=auth_header)

