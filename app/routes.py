from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, jsonify, Response, make_response
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST"])
def post_tasks():
    request_body = request.get_json()
    if "title" in request_body.keys() and "description" in request_body.keys() and "completed_at" in request_body.keys() :
        task = Task(title=request_body["title"],
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"],
                    )
        db.session.add(task)
        db.session.commit()
        return jsonify({"task": task.api_response()}), 201
    else:
        return make_response(
            {"details": "Invalid data"
            }
        ), 400

@goals_bp.route("", methods=["POST"])
def post_goals():
    request_body = request.get_json()
    if "title" in request_body.keys():
        goal = Goal(title=request_body["title"],
                    )
        db.session.add(goal)
        db.session.commit()
        return jsonify({"goal": goal.api_response()}), 201
    else:
        return make_response(
            {"details": "Invalid data"
            }
        ), 400

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    title_query = request.args.get("sort")
    if title_query == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.api_response())
    return jsonify(tasks_response), 200

@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.api_response())
    return jsonify(goals_response), 200

#filter
# Q1=Task.query.filter(db)....
# Q1.order_by(...)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response(jsonify(None), 404)
        # return make_response("",404)
        # return Response(None),404
        # return jsonify(None), 404
    return jsonify({"task": task.api_response()}), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response(jsonify(None), 404)
    return jsonify({"goal": goal.api_response()}), 200    

@tasks_bp.route("/<task_id>", methods=["PUT"])
def put_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return Response(None),404
    form_data = request.get_json()
    task.title = form_data["title"]
    task.description = form_data["description"]
    task.completed_at = form_data["completed_at"]
    db.session.commit()
    return jsonify({"task": task.api_response()}), 200 

@goals_bp.route("/<goal_id>", methods=["PUT"])
def put_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return Response(None),404
    form_data = request.get_json()
    goal.title = form_data["title"]
    db.session.commit()
    return jsonify({"goal": goal.api_response()}), 200 

def slack_bot_complete(task_title):
    # ## not working when key is hidden in .env
    return requests.post(("https://slack.com/api/chat.postMessage"), {
        'token': os.environ.get("slackbot_API_KEY"),
        'channel': "task-notifications",
        'text': f"Someone just completed {task_title}"
    }).json()

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return Response(None),404
    task.completed_at = datetime.now()
    db.session.commit()
    slack_bot_complete(task.title)
    return jsonify({"task": task.api_response(True)}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return Response(None),404
    task.completed_at = None
    db.session.commit()
    return jsonify({"task": task.api_response()}), 200    

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return Response(None),404
    db.session.delete(task)
    db.session.commit()
    return make_response(
        {"details": f'Task {task.id} "{task.title}" successfully deleted'
        }
    ), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return Response(None),404
    db.session.delete(goal)
    db.session.commit()
    return make_response(
        {"details": f'Goal {goal.id} "{goal.title}" successfully deleted'
        }
    ), 200