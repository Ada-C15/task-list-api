from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, request, jsonify
from datetime import datetime
import os, requests

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

#################### SLACK NOTIFICATIONS #################### 

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
URL = 'https://slack.com/api/chat.postMessage'

def send_notification_to_slack(msg):
    headers = {"Authorization": f'Bearer {SLACK_TOKEN}'}
    data = {"channel": CHANNEL_ID,"text": msg}
    return requests.post(URL, headers=headers, data=data)

######################## TASK ROUTES ######################## 

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    if len(request_body) < 3:
        return jsonify(details = f'Invalid data'), 400
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])  
    db.session.add(new_task)
    db.session.commit()
    send_notification_to_slack(f"New task created!")
    return jsonify(task=new_task.to_json()), 201

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def view_all_tasks():
    query_param_value = request.args.get("sort")
    tasks = Task.sort(query_param_value) # sort method called on the class
    view_tasks = [task.to_json() for task in tasks if tasks]
    return jsonify(view_tasks)

@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task = task.to_json())

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    updated_task = request.get_json()
    if not updated_task:
        return jsonify(None), 404
    task.title = updated_task['title']
    task.description = updated_task["description"]
    task.completed_at = updated_task["completed_at"]
    db.session.commit()
    send_notification_to_slack(f"Task {task_id} updated.")
    return jsonify(task=task.to_json())

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    send_notification_to_slack(f"Task {task_id} deleted.")
    return jsonify(details = f'Task {task.task_id} "{task.title}" successfully deleted')

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):
    send_notification_to_slack(f"Task {task_id} undone.")
    return mark_task(task_id, False) 

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):
    send_notification_to_slack(f"Task {task_id} completed!")
    return mark_task(task_id, True)

def mark_task(task_id, completed):
    task = Task.query.get(task_id)
    status = datetime.utcnow() if completed else None
    if task:
        task.completed_at = status
        db.session.commit()
        return jsonify(task=task.to_json())
    return jsonify(None), 404

######################## GOAL ROUTES ######################## 

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_new_goal():
    request_body = request.get_json()
    if len(request_body) < 1:
        return jsonify(details= f'Invalid data'), 400
    new_goal = Goal(title = request_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(goal=new_goal.to_json()), 201

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_goals():
    query_param_value = request.args.get("sort")
    goals = Goal.sort(query_param_value)
    view_goals= [goal.to_json() for goal in goals if goals]
    return jsonify(view_goals)

@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def view_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    return jsonify(goal=goal.to_json())

@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    updated_goal = request.get_json()
    if not updated_goal:
        return jsonify(None), 404
    goal.title = updated_goal["title"]
    db.session.commit()
    return jsonify(goal=goal.to_json())

@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted')

@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def create_new_task_in_goal(goal_id):
    request_body = request.get_json()
    if not request_body:
        return jsonify(None), 404
    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id) 
        task.goal_id = goal_id 
        db.session.commit()
    return jsonify(id=task.goal_id, task_ids=request_body["task_ids"]), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_task_for_specific_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    tasks = Task.query.filter_by(goal_id=int(goal_id))
    tasks_in_goal = [task.to_json() for task in tasks if tasks]
    return jsonify(id=int(goal_id), title=goal.title, tasks=tasks_in_goal)

