from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import asc, desc
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import requests
import os
import random

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


#=====================================================#
#                    TASK ROUTES                      #
#=====================================================#


@tasks_bp.route("", methods=["POST"])
def add_new_task():
    """
    Create a new Task
    """
    request_body = request.get_json()

    try:
        request_body["title"]
        request_body["description"]
        request_body["completed_at"]
    except:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_json()}, 201)


@tasks_bp.route("", methods=["GET"])
def list_all_tasks():
    """
    Get all Tasks in asc, desc, or unsorted order
    """
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(asc("title"))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc("title"))
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_json() for task in tasks]

    return jsonify(tasks_response)


@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    """
    Get one Task by id
    """
    task = Task.query.get(task_id)

    if task is None:
        return make_response("Task not found. Less to do then :)", 404)

    task_response = {"task": task.to_json()}
    return task_response


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task_by_id(task_id):
    """ 
    Update one Task by id
    """
    task = Task.query.get(task_id)

    if task is None:
        return make_response("Task not found. Less to do then :)", 404)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()

    return make_response({"task": task.to_json()})


@tasks_bp.route("/<int:task_id>/<complete_status>", methods=["PATCH"])
def patch_task_by_id(task_id, complete_status):
    """
    Marks a Task complete/incomplete & calls send_slack_notification function
    """
    task = Task.query.get(task_id)

    if task is None:
        return make_response("Task not found. Less to do then :)", 404)

    if complete_status == "mark_complete":
        task.completed_at = datetime.utcnow()
        send_slack_notification(task)
    else:
        task.completed_at = None

    db.session.commit()

    return make_response({"task": task.to_json()})


def send_slack_notification(task):
    """
    Requests Slack bot to send a notification for a completed Task
    """
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    AFFIRMATIONS = [
        "Your worth is not your productivity",
        "I see how much effort you've been putting in!",
        "Future you will thank you",
        "Remember, you deserve to take breaks"
    ]
    affirmation_quote = AFFIRMATIONS[random.randint(0,len(AFFIRMATIONS)-1)]
    text = (f"✅ Someone just completed the task {task.title}\n"
            f"❣️ {affirmation_quote}")

    query_params = {
        "channel": "task-notifications",
        "text": text
    }

    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }

    requests.post(PATH, params=query_params, headers=headers)


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task_by_id(task_id):
    """
    Delete one Task by id
    """
    task = Task.query.get(task_id)

    if task is None:
        return make_response("Task not found. Less to do then :)", 404)
    
    db.session.delete(task)
    db.session.commit()

    return make_response({
        "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    })


#=====================================================#
#                    GOAL ROUTES                      #
#=====================================================#


@goals_bp.route("", methods=["POST"])
def add_new_goal():
    """
    Create a new Goal
    """
    request_body = request.get_json()
    try:
        request_body["title"]
    except:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_json()}, 201)


@goals_bp.route("", methods=["GET"])
def list_all_goals():
    """
    Get all Goals in asc, desc, or unsorted order
    """
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(asc("title"))
    elif sort_query == "desc":
        goals = Goal.query.order_by(desc("title"))
    else:
        goals = Goal.query.all()

    goals_response = [goal.to_json() for goal in goals]

    return jsonify(goals_response)


@goals_bp.route("/<int:goal_id>", methods=["GET"])
def get_task_by_id(goal_id):
    """
    Get one Goal by id
    """
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("Goal not found.", 404)

    goal_response = {"goal": goal.to_json()}

    return goal_response


@goals_bp.route("/<int:goal_id>", methods=["PUT"])
def update_goal_by_id(goal_id):
    """ 
    Update one Goal by id
    """
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("Goal not found.", 404)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal": goal.to_json()})


@goals_bp.route("/<int:goal_id>", methods=["DELETE"])
def delete_goal_by_id(goal_id):
    """
    Delete one Task by id
    """
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("Goal not found.", 404)

    db.session.delete(goal)
    db.session.commit()

    return make_response({
        "details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'
    }, 200)


@goals_bp.route("/<int:goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    """
    Send a list of Task IDs to a one Goal
    """
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("Goal not found.", 404)

    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal_id

    db.session.commit()

    return make_response(jsonify(id=goal_id, task_ids=request_body["task_ids"]), 200)


@goals_bp.route("/<int:goal_id>/tasks", methods=["GET"])
def get_all_tasks_in_one_goal(goal_id):
    """
    Get all Tasks for one Goal 
    """
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("Goal not found.", 404)

    goal_response = goal.to_json()
    goal_response["tasks"] = [task.to_json() for task in goal.tasks]

    return jsonify(goal_response)
