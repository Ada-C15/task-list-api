import requests
from app import db
from flask import request, Blueprint, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc, asc
from dotenv import load_dotenv
import os
from app.slack_bot import slack_message
from datetime import datetime

load_dotenv()
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals") 

@tasks_bp.route("", methods = ["GET"])
def get_tasks():
    tasks_response = []
    order = request.args.get("sort")
    if order == "asc":
        tasks_query = Task.query.order_by(Task.title)
    else:
        tasks_query = Task.query.order_by(Task.title.desc())
    for task in tasks_query:
        tasks_response.append(task.build_dict())
    return jsonify(tasks_response), 200


@tasks_bp.route("", methods = ["POST"])
def add_tasks():
    request_body = request.get_json()
    if "title" not in request_body.keys() or "description" not in request_body.keys() or "completed_at" not in request_body.keys():
        return make_response({"details": "Invalid data"}, 400)
        
    new_task = Task(
        title=request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"],
    )
    slack_message(f"Someone just added {new_task.title} to the task list.")
    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.build_dict()}, 201


@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    return make_response(jsonify({"task":task.build_dict()}))
        

@tasks_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    form_data = request.get_json()
    task.title = form_data["title"]
    task.description = form_data["description"]
    task.completed_at = form_data["completed_at"]

    db.session.commit()

    return make_response(jsonify({"task":task.build_dict()}))

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}
    
@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = datetime.now()
        slack_message(f"Someone just completed {task.title}.")
        db.session.commit()
        return {"task": task.build_dict()}, 200
    else:
        return jsonify(None), 404


@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.completed_at:
            task.completed_at = None
        return jsonify({"task": task.build_dict()}), 200
    else:
        return jsonify(None), 404

@goals_bp.route("", methods = ["GET"])
def handle_goals():
    goals_query = Goal.query.all()
    goals_response = []
    for goal in goals_query:
        goals_response.append(goal.build_dict())
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    else:
        return ({"goal" : goal.build_dict()}, 200)

@goals_bp.route("", methods = ["POST"])
def post_goal():
    request_body = request.get_json()
    if "title" not in request_body.keys():
        return make_response({"details": "Invalid data"}, 400)
    new_goal = Goal(
        title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    return {"goal":new_goal.build_dict()}, 201

@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    form_data = request.get_json()
    goal.title = form_data["title"]
    db.session.commit()

    return make_response(jsonify({"goal":goal.build_dict()}))

@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    db.session.delete(goal)
    db.session.commit()

    return {"details" : f'Goal {goal_id} \"{goal.title}\" successfully deleted'}

@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def add_tasks_to_goals(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        request_body = request.get_json(goal)
        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal_id

        db.session.commit()

        return make_response(jsonify({"id": goal.goal_id, "task_ids": [task.task_id for task in goal.tasks]}))

@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks_for_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    tasks = [task.build_dict() for task in goal.tasks]
    goal_dict = goal.build_dict()
    goal_dict["tasks"] = tasks
    return goal_dict


        
    




      
