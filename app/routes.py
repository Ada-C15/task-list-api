from app import db 
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify, Flask # added Flask here bc ytube
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy # added from ytube vid, allows us to use the 1-to-many relationship
from sqlalchemy import desc, asc 
import os
from dotenv import load_dotenv
# requests allows us to make requests to other APIs. makes a request and returns the response from the external site
import requests # import here only? other files?

load_dotenv()

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

# TASK ROUTES
@task_bp.route("", methods=["POST"])
def create_task():
    """Create a task for the database"""
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_task = Task(title=request_body["title"], #value in db column reassigned with whatever user entered on their side
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"])
    
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task": new_task.to_json()}), 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    """Get multiple tasks per request"""
    tasks_ordered = request.args.get("sort")

    if not tasks_ordered:
        tasks = Task.query.all()
    elif tasks_ordered == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif tasks_ordered == "desc":
        tasks = Task.query.order_by(desc(Task.title))

    hold_tasks = []
    if not tasks:
        return jsonify(hold_tasks) 

    for task in tasks:
        hold_tasks.append(task.to_json())
    return jsonify(hold_tasks)

@task_bp.route("/<task_id>", methods=["GET"])
def get_single_task(task_id):
    single_task = Task.query.get(task_id)

    if not single_task:
        return make_response("", 404)
    return jsonify({"task": single_task.to_json()})

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task_element(task_id):
    """Overwrites a task with details provided by the user"""
    task = Task.query.get(task_id)

    if not task:
        return make_response("", 404)

    request_body = request.get_json()
    # reassign user's changes to the corresponding db field > cell
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()
    return jsonify({"task": task.to_json()})

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return make_response("", 404)
    
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return make_response("", 404)

    task.completed_at = datetime.now()
    db.session.commit()

    # Slack hookup
    target_url = "https://slack.com/api/chat.postMessage"
    LC_SLACK_KEY = os.environ.get("LC_SLACK_KEY")
    headers = {"Authorization": LC_SLACK_KEY}
    data = {
        "channel": "C0220R1781W", # copied from slack tester response body
        "text": f"Someone just completed the task {task.title}"}
    requests.patch(target_url, headers=headers, data=data)

    return jsonify({"task": task.to_json()})

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):

    task = Task.query.get(task_id)
    if not task:
        return make_response("", 404)

    task.completed_at = None
    db.session.commit()
    return jsonify({"task": task.to_json()})

# GOAL ROUTES
@goal_bp.route("", methods=["POST"])
def create_goal():
    """Create a goal for the database"""
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal": new_goal.to_json()}), 201

@goal_bp.route("", methods=["GET"])
def get_goals():
    """Get multiple goals per request"""
    hold_goals = []
    goals = Goal.query.all()
    if not goals:
        return jsonify(hold_goals)
    for goal in goals:
        hold_goals.append(goal.to_json())
        return jsonify((hold_goals))

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_single_goal(goal_id):
    single_goal = Goal.query.get(goal_id)
    if not single_goal:
        return make_response("", 404)
    return jsonify({"goal": single_goal.to_json()})

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return make_response("", 404)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return jsonify({"goal": goal.to_json()})

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return make_response("", 404)
    db.session.delete(goal)
    db.session.commit()
    return make_response({'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)

# @goal_bp.route("/<goal_id>/tasks", methods=["POST"])
# def create_goal_w_tasks(goal_id, task_list):
#     """Updates goal with related tasks"""
#     request_body = request.get_json() # {"task_ids": [1, 2, 3]}
#     target_goal = Goal.query.get(goal_id) # get the target goal
#     target_goal.tasks = request_body["task_ids"] # assign user's tasks to new db column
#     db.session.commit() # commit the change to the attr
#     return jsonify(target_goal.to_json())