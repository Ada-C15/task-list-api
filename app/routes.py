from app import db
from .models.task import Task
from .models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from sqlalchemy import desc, asc
import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@task_bp.route("", methods=["POST", "GET"])
def tasks():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        else:
            new_task = Task(title = request_body["title"],
                        description = request_body["description"],
                        completed_at = request_body["completed_at"])
            db.session.add(new_task)
            db.session.commit()

            return jsonify({"task":new_task.to_dict()}), 201

    elif request.method == "GET":
        sort_by = request.args.get("sort")
        if sort_by == "asc": 
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif sort_by == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
        else: 
            tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.to_dict())

        return jsonify(tasks_response), 200

@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response(), 404
    
    elif request.method == "GET":
        if task.assoc_goal == None:
            return jsonify({"task":task.to_dict()}), 200
        else:
            return jsonify({"task":task.to_dict_goal()}), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}),200

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()

        return jsonify({"task":task.to_dict()}), 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response(), 404

    task.completed_at = datetime.datetime.now()
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    slack_headers = {'Authorization': "SLACK_BOT_TOKEN"}
    slack_params = {'channel':'task-notifications',
            'text': f'Someone just completed the task {task.description}',
            'format': "json"}
    requests.post(url, headers=slack_headers, params=slack_params)

    return jsonify({"task":task.to_dict()}), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response(), 404

    task.completed_at = None
    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

@goal_bp.route("", methods=["POST", "GET"])
def goals():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        else:
            new_goal = Goal(title = request_body["title"],)
            db.session.add(new_goal)
            db.session.commit()

            return jsonify({"goal":new_goal.to_dict()}), 201

    elif request.method == "GET":
        goals = Goal.query.all()
        goals_response = []
        for goal in goals:
            goals_response.append(goal.to_dict())

        return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal == None:
        return make_response(), 404
    
    elif request.method == "GET":
        return jsonify({"goal":goal.to_dict()}), 200

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}),200

    elif request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data["title"]
        db.session.commit()

        return jsonify({"goal":goal.to_dict()}), 200


@goal_bp.route("/<goal_id>/tasks", methods=["GET", "POST"])
def tasks_to_goals(goal_id):
    goal = Goal.query.get(goal_id)

    if goal == None:
        return make_response(), 404
    
    elif request.method == "POST":
        form_data = request.get_json() 
        task_list = form_data["task_ids"]

        for task in task_list:
            task = Task.query.get(task)
            task.assoc_goal = goal.goal_id
            
        db.session.commit()
        return jsonify({"id": goal.goal_id,
                        "task_ids": task_list}), 200

    elif request.method == "GET":
        tasks = Task.query.filter_by(assoc_goal=goal_id).all()

        assoc_task_list = []
        for task in tasks:
            assoc_task_list.append(task.to_dict_goal())

        return jsonify({"id": goal.goal_id,
                        "title": goal.title,
                        "tasks": assoc_task_list}), 200



