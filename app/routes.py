from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import desc, asc
from datetime import datetime
import os
import slack

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    request_body = request.get_json()
    
    try:
        new_goal = Goal(title=request_body["title"])

    except KeyError:
        return make_response({
            "details": "Invalid data"
        }, 400)

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_json()
    }, 201

@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def get_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if goal == None:
        return make_response("", 404)

    return {
        "goal": goal.to_json()}, 200

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def goals_index():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())

    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    form_data = request.get_json()

    if goal == None:
        return make_response("", 404)
    
    goal.title = form_data["title"]

    db.session.commit()

    return {
        "goal": goal.to_json()
    }, 200

@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if not goal:
        return make_response("", 404)
    
    db.session.delete(goal)
    db.session.commit()

    return make_response({
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    })


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def tasks_index():
    sort_type = request.args.get("sort")

    if sort_type == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_type == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    else:
        tasks = Task.query.all()
    
    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200
    
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_one_task(task_id):
    task = Task.query.get(task_id)
    
    if task == None:
        return make_response("", 404)

    return {
        "task": task.to_json()}, 200
        

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

    except KeyError:
        return make_response({
            "details": "Invalid data"
        }, 400)

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_json()
    }, 201

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    form_data = request.get_json()

    if task == None:
        return make_response("", 404)
    
    task.title = form_data["title"]
    task.description = form_data["description"]
    task.is_complete = form_data["completed_at"]

    db.session.commit()

    return {
        "task": task.to_json()
    }, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    task = Task.query.get(task_id)
    
    if not task:
        return make_response("", 404)
    
    db.session.delete(task)
    db.session.commit()

    return make_response({
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    })

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def task_mark_complete(task_id):
    task = Task.query.get(task_id)
    current_datetime = datetime.utcnow()
    
    if not task:
        return make_response("", 404)
    else:
        task.completed_at = current_datetime
    
    db.session.commit()
    
    client = slack.WebClient(os.environ["SLACK_TOKEN"])
    client.chat_postMessage(
            channel="task-notifications",
            text=f"Someone just completed the task {task.title}")
            
    return {
        "task": task.to_json()
    }, 200

    
        
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def task_mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if not task:
        return make_response("", 404)
    elif task.completed_at != None:
        task.completed_at = None

    db.session.commit()

    return {
        "task": task.to_json()
    }, 200