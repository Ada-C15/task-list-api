import os
import requests
from datetime import datetime
from flask import Blueprint, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc

from app import db
from app.models.goal import Goal
from app.models.task import Task


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")


@task_bp.route("", methods=["GET"])
def task():
    tasks = Task.query.all()
    task_response = []

    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    for task in tasks:
        task_response.append(task.to_json())

    return jsonify(task_response), 200


@task_bp.route("/<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.filter_by(task_id=id).first()
    if task == None:
        return make_response(f"Task {id} not found", 404)
    else:
        return jsonify({"task": task.to_json()}), 200


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:

        t = Task(title=request_body["title"],
                 description=request_body["description"],
                 completed_at=request_body["completed_at"])
    except KeyError:
        return make_response({
            "details": "Invalid data"
        }, 400)

    db.session.add(t)
    db.session.commit()
    return {
        "task": t.to_json()
    }, 201


@task_bp.route("/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get(id)
    if task == None:
        return make_response(f"Task {id} not found", 404)
    else:
        update_body = request.get_json()
        task.title = update_body["title"]
        task.description = update_body["description"]
        db.session.commit()
        return make_response({"task": task.to_json()}, 200)


@task_bp.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get(id)
    if task == None:
        return make_response(f"Task {id} not found", 404)
    else:
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f"Task {id} \"{task.title}\" successfully deleted"}, 200)


@task_bp.route("/<int:id>/mark_complete", methods=["PATCH"])
def complete_task(id):
    task = Task.query.get(id)
    if task == None:
        return make_response(f"Task {id} not found", 404)
    else:
        task.completed_at = datetime.now()
        db.session.commit()

        if os.environ.get("SLACK_API_TOKEN") != None:
            msg = "Someone just completed the task " + task.title
            slack_headers = {"Authorization": "Bearer " +
                             os.environ.get("SLACK_API_TOKEN")}
            slack_params = {"channel": "task-notifications", "text": msg}
            resp = requests.post("https://slack.com/api/chat.postMessage",
                                 params=slack_params, headers=slack_headers)

        return make_response({"task": task.to_json()}, 200)


@task_bp.route("/<int:id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(id):
    task = Task.query.get(id)
    if task == None:
        return make_response(f"Task {id} not found", 404)
    else:
        task.completed_at = None
        db.session.commit()
        return make_response({"task": task.to_json()}, 200)

# End of Wave 1 - 4
# Beginning of Wave 5


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        goal = Goal(title=request_body["title"])
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(goal)
    db.session.commit()
    return jsonify({"goal": goal.to_json()}), 201


@goal_bp.route("/<int:id>", methods=["PUT"])
def update_goal(id):
    goal = Goal.query.get(id)
    if not goal:
        return make_response('Goal not found.', 404)
    request_body = request.get_json()
    goal.title = request_body['title']
    db.session.commit()
    return jsonify({'goal': goal.to_json()}), 200


@goal_bp.route("/<int:id>", methods=["GET"])
def get_goal(id):
    goal = Goal.query.filter_by(id=id).first()
    if goal == None:
        return make_response(f"Goal {id} not found", 404)
    else:
        return jsonify({"goal": goal.to_json()}), 200


@goal_bp.route("", methods=["GET"])
def goal():
    goals = Goal.query.all()
    goal_response = []

    for goal in goals:
        goal_response.append(goal.to_json())

    return jsonify(goal_response), 200


@goal_bp.route("/<int:id>", methods=["DELETE"])
def delete_goal(id):
    goal = Goal.query.get(id)
    if goal == None:
        return make_response(f"Goal {id} not found", 404)
    db.session.delete(goal)
    db.session.commit()
    return make_response({"details": f"Goal {id} \"{goal.title}\" successfully deleted"}, 200)

# End of Wave 5

# Beginning of Wave 6

@goal_bp.route("/<int:id>/tasks", methods=["GET", "POST"])
def goal_tasks_list(id):
    goal = Goal.query.get(id)
    if not goal:
        return make_response('Goal doesn\'t exist', 404)

    if request.method == 'POST':
        task_ids = request.get_json()['task_ids']
        for task_id in task_ids:
            task = Task.query.get(task_id)
            if task not in goal.tasks:
                goal.tasks.append(task)

        response_body = {
            'id': goal.id,
            'task_ids': [task.task_id for task in goal.tasks]
        }
        db.session.commit()
        return jsonify(response_body), 200


    tasks = []
    for task in goal.tasks:
        task_json = {
            'id': task.task_id,
            'goal_id': task.goal_id,
            'title': task.title,
            'description': task.description,
            'is_complete': task.is_complete(),
        }
        tasks.append(task_json)


    response_body = {
        'id': goal.id,
        'title': goal.title,
        'tasks': tasks,
    }

    return jsonify(response_body), 200
#Ending of wave 6