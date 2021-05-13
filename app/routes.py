from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request
from flask import request, Blueprint, make_response
from flask import jsonify
from datetime import datetime 
from sqlalchemy import asc, desc
import requests
import json
import os

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_single_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    complete = task.completed_at_helper()  # Helper function to return boolean

    if request.method == "GET":
        return jsonify({"task": task.json_object()}), 200

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.is_complete = form_data["completed_at"] 

        db.session.commit()
        return jsonify({"task": task.json_object()}),200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200


@task_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        
        request_value = request.args.get("sort") 
        
        if request_value == None:
            tasks = Task.query.all()

        if request_value == "asc":
            tasks = Task.query.order_by(Task.title.asc()) 
        
        
        if request_value == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        task_response = []

        for task in tasks:
        
            task_response.append(task.json_object())
        
        return jsonify(task_response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "completed_at" not in request_body or "description" not in request_body or "title" not in request_body:
            return jsonify({
                "details": "Invalid data"
            }), 400

        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({"task": new_task.json_object()}), 201

        db.session.add(new_task)
        db.session.commit()

def slack_bot(task):
    url = "https://slack.com/api/chat.postMessage?channel=task-notifications"
    slack_token = os.environ.get("SLACK")

    payload = {"text": f"Someone just completed the task: '{task.title}'!"}
    headers = {"Authorization": f"Bearer {slack_token}"}

    return requests.request("PATCH", url, headers=headers, data=payload)


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):
    
    if request.method == "PATCH":
        
        task = Task.query.get(task_id)
        
        if task is None:
            return jsonify(None), 404
        
        task.completed_at = datetime.now()

    
        db.session.commit()
        
        # call slackbot
        slack_bot(task)

        
        return jsonify({"task": task.json_object()}),200 


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):
    
    if request.method == "PATCH":
        
        task = Task.query.get(task_id)
        
        if task is None:
            return jsonify(None), 404
        
        task.completed_at = None
        
        return jsonify({"task":task.json_object()}),200
    
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")
@goal_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    if request.method == "GET":
        return jsonify({"goal": goal.goal_json_object()}), 200

    elif request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data["title"]
        
        db.session.commit()
        return jsonify({"goal": goal.goal_json_object()}),200

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        
        return jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}), 200

@goal_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def one_goal():
    if request.method == "GET":
        goals = Goal.query.all()
        
        goal_response = []

        for goal in goals:
            goal_response.append(goal.goal_json_object())
        
        return jsonify(goal_response), 200

    if request.method == "POST":
        request_body = request.get_json() 
        
        if request_body == {}:    
            return jsonify({"details": f'Invalid data'}), 400
        
        new_goal = Goal(title=request_body["title"])

        db.session.add(new_goal)
        db.session.commit()
        
        return jsonify({"goal":new_goal.goal_json_object()}),201
    