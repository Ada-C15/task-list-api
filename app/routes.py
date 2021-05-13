from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, request, jsonify
from datetime import datetime
import os, requests

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

######################## TASK CRUD OPERATIONS ######################## 

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    response_body = request.get_json()
    if len(response_body) < 3:
        return jsonify(details = f'Invalid data'), 400
    new_task = Task(title=response_body["title"],
                    description=response_body["description"],
                    completed_at=response_body["completed_at"])  
    db.session.add(new_task)
    db.session.commit()
    send_new_task_notification()
    return jsonify(task=new_task.to_json()), 201

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def view_all_tasks():
    query_param_value = request.args.get("sort")
    if query_param_value == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif query_param_value == "asc":
        tasks = Task.query.order_by(Task.title).all()
    else:
        tasks = Task.query.all()
    tasks_view = []
    if tasks:
        for task in tasks:
            tasks_view.append(task.to_json())
    return jsonify(tasks_view)

@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def view_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    return jsonify(task = task.to_json())

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    updated_task = request.get_json()
    if not task or not updated_task:
        return jsonify(None), 404
    task.title = updated_task['title']
    task.description = updated_task["description"]
    task.completed_at = updated_task["completed_at"]
    db.session.commit()
    return jsonify(task=task.to_json())

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    db.session.delete(task)
    db.session.commit()
    send_deleted_notification(task_id)
    return jsonify(details = f'Task {task.task_id} "{task.title}" successfully deleted')

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):
    send_undone_notification(task_id)
    return mark_task(task_id, False) 

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):
    send_completed_notification(task_id)
    return mark_task(task_id, True)

def mark_task(task_id, completed):
    task = Task.query.get(task_id)
    status = datetime.utcnow() if completed else None
    if task:
        task.completed_at = status
        db.session.commit()
        return jsonify(task=task.to_json())
    return jsonify(None), 404

######################## GOAL CRUD OPERATIONS ######################## 

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_new_goal():
    response_body = request.get_json()
    if len(response_body) < 1:
        return jsonify(details= f'Invalid data'), 400
    new_goal = Goal(title = response_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(goal=new_goal.to_json()), 201

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_goals():
    goals = Goal.query.all()
    response_body = [] 
    for goal in goals:
        response_body.append(goal.to_json())
    return jsonify(response_body)

@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def view_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify(None), 404
    return jsonify(goal=goal.to_json())

@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    updated_goal = request.get_json()
    if not goal or not updated_goal:
        return jsonify(None), 404
    goal.title = updated_goal["title"]
    db.session.commit()
    return jsonify(goal=goal.to_json())

@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify(None), 404
    db.session.delete(goal)
    db.session.commit()
    return jsonify(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted')

@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def create_new_task_in_goal(goal_id):
    response_body = request.get_json()
    if not response_body:
        return jsonify(None), 404
    for task_id in response_body["task_ids"]:
        task = Task.query.get(task_id) 
        task.goal_id = goal_id 
        db.session.commit()
    return jsonify(id=task.goal_id, task_ids=response_body["task_ids"]), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_task_for_specific_goal(goal_id):
    goal = Goal.query.get(goal_id)
    tasks = Task.query.filter_by(goal_id=int(goal_id))
    if not goal:
        return jsonify(None), 404
    task_list = []
    for task in tasks:
        task_list.append(task.to_json())
    return jsonify(id=int(goal_id), title=goal.title, tasks=task_list)

#################### SLACK NOTIFICATIONS METHODS #################### 

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
URL = 'https://slack.com/api/chat.postMessage'

headers = {"Authorization": f'Bearer {SLACK_TOKEN}'}
data = {"channel": CHANNEL_ID,"text": None}

def send_new_task_notification():
    data["text"] = f"New task created!"
    return requests.post(URL, headers=headers, data=data)
    
def send_completed_notification(task_id):
    data["text"] = f"Task {task_id} completed!"
    return requests.post(URL, headers=headers, data=data)

def send_undone_notification(task_id):
    data["text"] = f"Task {task_id} undone."
    return requests.post(URL, headers=headers, data=data)

def send_deleted_notification(task_id):
    data["text"] = f"Task {task_id} deleted."
    return requests.post(URL, headers=headers, data=data)
