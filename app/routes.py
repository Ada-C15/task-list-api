from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc, asc 
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    order_query = request.args.get("sort")
    if order_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif order_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return make_response(jsonify(tasks_response), 200)

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" in request_body and "description" in request_body and "completed_at" in request_body:
        new_task = Task(title = request_body["title"],
                        description = request_body["description"],
                        completed_at=request_body["completed_at"])
        db.session.add(new_task)
        db.session.commit()
        return make_response({"task": new_task.to_dict()}, 201) 
    else:
        return make_response({"details": "Invalid data"}, 400)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return {"task": task.to_dict()}, 200
    else:
        return make_response("", 404)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return make_response({"task": task.to_dict()}, 200)
    else:
        return make_response("", 404)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200)
    else:
        return make_response("", 404)

@tasks_bp.route("/<task_id>/<mark_status>", methods=["PATCH"])
def handle_task_completion(task_id, mark_status):
    task = Task.query.get(task_id)
    if task:
        if mark_status == "mark_incomplete":
            task.completed_at = None
            db.session.commit()
            return make_response({"task": task.to_dict()}, 200)
        elif mark_status == "mark_complete":
            task.completed_at = datetime.utcnow()
            db.session.commit()
            send_slack_message(task.title)
            return make_response({"task": task.to_dict()}, 200)
    else:
        return make_response("", 404)


#WAVE 4
# consider moving to a "utilities" folder in refactoring
PATH = "https://slack.com/api/chat.postMessage"

def send_slack_message(task_title):
    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task_title}"
    }
    slackbot_token = os.environ.get('SLACK_API_KEY')
    header = {
        "Authorization": f"Bearer {slackbot_token}"
    }
    requests.post(PATH, params=query_params, headers=header)


#WAVE 5 
@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return make_response(jsonify(goals_response), 200)

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" in request_body:
        new_goal = Goal(title = request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        return make_response({"goal": new_goal.to_dict()}, 201) 
    else:
        return make_response({"details": "Invalid data"}, 400)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        return {"goal": goal.to_dict()}, 200
    else:
        return make_response("", 404)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        form_data = request.get_json()
        goal.title = form_data["title"]
        db.session.commit()
        return make_response({"goal": goal.to_dict()}, 200) 
    else:
        return make_response("", 404)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        db.session.delete(goal)
        db.session.commit()
        return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}, 200)
    else:
        return make_response("", 404)

# WAVE 06
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    request_body = request.get_json()
    tasks_for_goal = request_body["task_ids"]
    for task_id in tasks_for_goal:
        task = Task.query.get(task_id)
        task.goal_id = int(goal_id)
    return make_response({
        "id": int(goal_id),
        "task_ids": tasks_for_goal
    }, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not Goal.query.get(goal_id):
        return make_response("404"), 404
    else:
        tasks_response = []
        tasks_of_goal = Task.query.filter_by(goal_id=goal_id)
        if tasks_of_goal:
            for task in tasks_of_goal:
                tasks_response.append(task.to_dict())
        return make_response({
            "id": int(goal_id),
            "title": goal.title,
            "tasks": tasks_response
            }, 200)