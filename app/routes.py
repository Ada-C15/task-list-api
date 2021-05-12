from app.models.task import Task
from app.models.goal import Goal

from app import db
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@tasks_bp.route("/<task_id>/<status>", methods=["PATCH"], strict_slashes=False)
def patch_status(task_id, status):

    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None),404

    if status == 'mark_complete':
        date = datetime.today()
        task.completed_at = date
        slack_post_message(task.title)

    else: 
        task.completed_at = None

    db.session.commit()
    return {
        "task": task.get_resp()
    },200

def slack_post_message(title):
    url = 'https://slack.com/api/chat.postMessage'
    params = {
        "channel":"task-notification",
        "text":f"Someone just completed the task {title}"
    }
    header={
        "Authorization": f"Bearer {os.environ.get('API_TOKEN')}" }

    req = requests.post(url, params=params, headers=header)
    r = req.json()

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_single_task(task_id):

    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None),404

    if request.method == "GET":
        return {"task": task.get_resp()}, 200

    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return {"task": task.get_resp()}, 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {
            "details":f'Task {task.task_id} "{task.title}" successfully deleted'
        }, 200

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        
        if sort_query == 'asc':
            tasks = Task.query.order_by(Task.title.asc())
        elif sort_query == 'desc':
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.all()
        
        task_response = []
        for task in tasks:
            task_response.append(task.get_resp())
        return jsonify(task_response), 200
    
    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return {"details":"Invalid data"}, 400

        else:
            new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()
        return {"task": new_task.get_resp()}, 201

@goals_bp.route("", methods=["GET","POST"])
def handle_goals():
    if request.method == "GET":
        goals = Goal.query.all()
        goal_response = []
        for goal in goals:
            goal_response.append(goal.get_resp())
        return jsonify(goal_response), 200

    elif request.method == "POST":    
        request_body = request.get_json()
        if "title" not in request_body:
            return {"details":"Invalid data"}, 400
        else:
            new_goal = Goal(title=request_body["title"])

            db.session.add(new_goal)
            db.session.commit()
            return {"goal": new_goal.get_resp()}, 201

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_single_goal(goal_id):

    goal = Goal.query.get(goal_id)
    if goal is None:
        return jsonify(None),404

    if request.method == "GET":
        return {"goal": goal.get_resp()}, 200

    elif request.method == "PUT":
        form_data = request.get_json()
        goal.title = form_data["title"]
        db.session.commit()
        return {"goal": goal.get_resp()}, 200

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return {
            "details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
        }, 200

@goals_bp.route("/<goal_id>/<tasks>", methods=["GET","POST"], strict_slashes=False)
def retrieve_tasks(goal_id, tasks):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None),404

    request_body = request.get_json()

    if request.method == "GET":

        tasks_list = []
        tasks = goal.tasks

        for task in tasks:
            tasks_list.append((task.get_resp()))
        goal_dict = goal.get_resp()
        goal_dict["tasks"] = tasks_list
        return jsonify(goal_dict), 200

    elif request.method == "POST":
        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = int(goal_id)

        db.session.commit()
        return jsonify({
                "id": int(goal_id),
                "task_ids": request_body["task_ids"]
            }), 200