from flask import request, Blueprint, make_response
from app import db, slack_token
from .models.task import Task
from .models.goal import Goal
from flask import jsonify
from datetime import datetime
import requests, json

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST"])
def add_task():

    request_body = request.get_json()
    title = request_body.get("title")
    description = request_body.get("description")
    completed_at = request_body.get("completed_at")

    if not title or not description or "completed_at" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task(title=title,
                    description=description,
                    completed_at=completed_at)
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json()}), 201


@tasks_bp.route("", methods=["GET"])
def get_task():
    tasks = Task.query.all()
    tasks_response = []

    sort = request.args.get("sort")
    if sort == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200


@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_single_task(task_id):

    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    tasks = Task.query.filter_by(goal_id=Goal.goal_id)
    
    if task.goal_id is not None:
        # task_response =[]
        for tas in tasks:
            tasks_dict = tas.to_json()
            tasks_dict["goal_id"] = task.goal_id
            return jsonify({"task": tasks_dict})

            # task_response.append(tasks_dict)
        return jsonify({"task": task_response}), 200


    if task:
        return jsonify({"task": task.to_json()}), 200

    return make_response("", 404)


@tasks_bp.route("/<int:task_id>/mark_complete", methods=["PATCH"])
def update_completed_at(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    task.completed_at = datetime.utcnow()

    db.session.commit()

    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {slack_token}"
    }
    slack_data = {
        "channel": "C021RGYNY48",
        "text": f"Someone just completed the task {task.title}"
    }
    requests.post(slack_url, json=slack_data, headers=headers)

    return jsonify({"task" :task.to_json()}), 200


@tasks_bp.route("/<int:task_id>/mark_incomplete", methods=["PATCH"])
def update_not_completed_at(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    task.completed_at = None

    return jsonify({"task" :task.to_json()}), 200



@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": task.to_json()}), 200

@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "details": f'Task {task_id} \"Go on my daily walk 🏞\" successfully deleted'
    })


@goals_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()
    title = request_body.get("title")

    if not title:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal(title=title)
    
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_json()}), 201


@goals_bp.route("", methods=["GET"])
def get_goal():
    goals = Goal.query.all()
    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_json())

    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal:
        return jsonify({"goal": goal.to_json()}), 200

    return make_response("", 404)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": goal.to_json()}), 200    


@goals_bp.route("<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({
        "details": f'Goal {goal_id} \"Build a habit of going outside daily\" successfully deleted'
    })



@goals_bp.route("<goal_id>/tasks", methods=["GET", "POST"])
def goal_to_task(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    if request.method == "GET":
        tasks = Task.query.filter_by(goal_id=goal.goal_id)
        tasks_reponse = []
        for task in tasks:
            tasks_dict = task.to_json()
            tasks_dict["goal_id"] = goal.goal_id
            tasks_reponse.append(tasks_dict)

        return jsonify({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": tasks_reponse
        }), 200

    if request.method == "POST":
        request_body = request.get_json()

        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal.goal_id

        return jsonify({"id": goal.goal_id,
                "task_ids": request_body["task_ids"]
        }), 200

