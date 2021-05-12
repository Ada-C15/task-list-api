import requests
import os
from flask import request, Blueprint, make_response, jsonify

from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix= "/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def create_task():

    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        else:
            new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])

            db.session.add(new_task)
            db.session.commit()

            return make_response({
                "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": new_task.task_completed()
                }
            }, 201)
    
    elif request.method == "GET":       
        task_query = request.args.get("sort")
        if task_query == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif task_query == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all() 
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.task_completed()
            })
        return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def specific_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response(), 404
    
    elif request.method == "GET":

        if task.goal == None:
            return jsonify({
                "task": {
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": task.task_completed()
                }
            }), 200

        else:
            return jsonify({
                "task": {
                    "id": task.task_id,
                    "goal_id": task.goal_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": task.task_completed()
                }
            }), 200

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()

        return jsonify({
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.task_completed()
            }
        }), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200 

def slack_message_bot(task):

    params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.task_id}"
    }

    headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_API_KEY')}"
    }

    requests.post("https://slack.com/api/chat.postMessage", data=params, headers=headers)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    
    if task == None:
        return make_response(), 404
    
    task.completed_at = datetime.utcnow()
    db.session.commit()

    slack_message_bot(task)

    return jsonify({
        "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.task_completed()
        }
        }), 200
    
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response(), 404
    
    task.completed_at = None
    db.session.commit()

    return jsonify({
            "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.task_completed()
            }
            }), 200

goals_bp = Blueprint("goals", __name__, url_prefix= "/goals")
@goals_bp.route("", methods=["POST", "GET"])
def create_goal():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        else:
            new_goal = Goal(title=request_body["title"])

            db.session.add(new_goal)
            db.session.commit()

        return make_response({
            "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title,
            }
        }, 201)
    
    elif request.method == "GET":
        goals = Goal.query.all()
        goals_response = []

        for goal in goals:
            goals_response.append({
                "id": goal.goal_id,
                "title": goal.title
            })
        
        return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def specific_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal == None:
        return make_response(), 404
    
    elif request.method == "GET":
        return jsonify({
            "goal": {
                "id": goal.goal_id,
                "title": goal.title
            }
        }), 200
    
    elif request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data["title"]
        db.session.commit()

        return jsonify({
            "goal": {
                "id": goal.goal_id,
                "title": goal.title
            }
        }), 200

    
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}), 200

@goals_bp.route("<goal_id>/tasks", methods=["POST", "GET"])
def goal_to_task(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    if request.method == "POST":
        request_body = request.get_json()

        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal.goal_id

        return jsonify({
            "id": goal.goal_id,
            "task_ids": request_body["task_ids"]
        }), 200


    elif request.method == "GET":
        tasks = Task.query.filter_by(goal_id=goal.goal_id)

        connected_tasks = []
        for task in tasks:
            connected_tasks.append({
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.task_completed(),
        })

        return jsonify({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": connected_tasks
        }), 200












