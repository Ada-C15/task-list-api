from app import db
from flask import Blueprint
from flask import request, Blueprint, make_response
from flask import jsonify
from .models.goal import Goal
from .models.task import Task
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST", "GET"])
def tasks_functions():
    if request.method == "POST":
        req_body = request.get_json()
        if "title" not in req_body or "description" not in req_body or "completed_at" not in req_body:
            return {
                "details": "Invalid data"
            }, 400
        new_task = Task(title = req_body["title"], description = req_body["description"], completed_at = req_body["completed_at"])
        db.session.add(new_task)
        db.session.commit()
        response_body = {
            "task": new_task.to_json()
        }
        return jsonify(response_body), 201

    elif request.method == "GET":
        order = request.args.get("sort")
        if order == "asc":
            new_order = Task.query.order_by(Task.title.asc())
            response = []
            for task in new_order:
                response.append(task.to_json())
            return jsonify(response), 200

        elif order == "desc":
            new_order = Task.query.order_by(Task.title.desc())
            response = []
            for task in new_order:
                response.append(task.to_json())
            return jsonify(response), 200

        all_tasks = Task.query.all()
        response_body = []
        for any_task in all_tasks:
            response_body.append(any_task.to_json())
        return jsonify(response_body), 200

@tasks_bp.route("/<task_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def dealing_with_id(task_id):
    a_task = Task.query.get(task_id)

    if a_task is None:
        return make_response("", 404)
    
    if request.method == "GET":
        return {
            "task": a_task.to_json()
        }, 200
    
    elif request.method == "PUT":
        info = request.get_json()

        a_task.title = info["title"]
        a_task.description = info["description"]
        a_task.completed_at = info["completed_at"]

        db.session.commit()
        return {
            "task": a_task.to_json()
        }, 200
    
    elif request.method == "DELETE":
        db.session.delete(a_task)
        db.session.commit()
        return {
            "details": f"Task {a_task.task_id} \"{a_task.title}\" successfully deleted"
        }, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def make_task_complete(task_id):
    id = Task.query.get(task_id)

    if id is None:
        return make_response("", 404)

    id.completed_at = datetime.now()
    db.session.commit()
    response_body = {
        "task": id.to_json()
    }

    path = "https://slack.com/api/chat.postMessage"
    text_response = f"Someone just completed the task {id.title}"
    query_params = {
        "channel": "task-notifications",
        "text": text_response
    }
    header = {
        "Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"
    }
    response = requests.post(path, params=query_params, headers=header)
    

    return jsonify(response_body), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def make_task_incomplete(task_id):
    id = Task.query.get(task_id)

    if id is None:
        return make_response("", 404)

    id.completed_at = None
    db.session.commit()
    response_body = {
        "task": id.to_json()
    }
    return jsonify(response_body), 200
    
#Goals routes***********************************************************************************************************************
@goals_bp.route("", methods=["GET", "POST"])
def handle_goals():
    if request.method == "POST":
        req_body = request.get_json()
        if "title" not in req_body:
            return {
                "details": "Invalid data"
            }, 400
        new_goal = Goal(title = req_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        response_body = {
            "goal": new_goal.goal_json()
        }
        return jsonify(response_body), 201
    
    if request.method == "GET":
        all_goals = Goal.query.all()
        response_body = []
        for any_goal in all_goals:
            response_body.append(any_goal.goal_json())
        return jsonify(response_body), 200

@goals_bp.route("/<goal_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def goal_id_functions(goal_id):
    a_goal = Goal.query.get(goal_id)

    if a_goal is None:
        return make_response("", 404)
    
    if request.method == "GET":
        return {
            "goal": a_goal.goal_json()
        }, 200
    
    elif request.method == "PUT":
        info = request.get_json()
        a_goal.title = info["title"]
        db.session.commit()
        return {
            "goal": a_goal.goal_json()
        }, 200
    
    elif request.method == "DELETE":
        db.session.delete(a_goal)
        db.session.commit()
        return {
            "details": f"Goal {a_goal.goal_id} \"{a_goal.title}\" successfully deleted"
        }, 200