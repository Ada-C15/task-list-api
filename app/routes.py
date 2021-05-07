from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc, asc 
from datetime import datetime

#why don't I need to say from ... import ... here???
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():

    if request.method == "GET":
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

    else: 
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


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task:
        if request.method == "GET":
            return {"task": task.to_dict()}, 200

        elif request.method == "PUT":
            form_data = request.get_json()
            task.title = form_data["title"]
            task.description = form_data["description"]
            task.completed_at = form_data["completed_at"]
            db.session.commit()
            return make_response({"task": task.to_dict()}, 200)
        
        elif request.method == "DELETE":
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
            #call to function that sends slack message
            send_slack_message(task.title)
            return make_response({"task": task.to_dict()}, 200)
    else:
        return make_response("", 404)


#WAVE 4 -- for organization sake should this go somewhere else?
PATH = "https://slack.com/api/chat.postMessage"

#define a function that sends a slack message 
def send_slack_message(task_title):
    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task_title}"
    }
    slackbot_token = os.environ.get('SLACK_API_KEY')
    header = {
        "Authorization": f"Bearer {slackbot_token}"
    }
    # why use .POST and not .PATCH
    requests.post(PATH, params=query_params, headers=header)


#WAVE 5 
@goals_bp.route("", methods=["GET", "POST"])
def handle_goals():
    if request.method == "GET":
        goals = Goal.query.all()
        goals_response = []
        for goal in goals:
            goals_response.append(goal.to_dict())
        return make_response(jsonify(goals_response), 200)

    else: 
        request_body = request.get_json()
        if "title" in request_body:
            new_goal = Goal(title = request_body["title"])
            db.session.add(new_goal)
            db.session.commit()
            return make_response({"goal": new_goal.to_dict()}, 201) 
        else:
            return make_response({"details": "Invalid data"}, 400)

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        if request.method == "GET":
            return {"goal": goal.to_dict()}, 200
        elif request.method == "PUT":
            form_data = request.get_json()
            goal.title = form_data["title"]
            db.session.commit()
            return make_response({"goal": goal.to_dict()}, 200) 
        elif request.method == "DELETE":
            db.session.delete(goal)
            db.session.commit()
            return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}, 200)
    else:
        return make_response("", 404)