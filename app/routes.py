from flask import Blueprint
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, make_response, jsonify, request
from app import db
from sqlalchemy import asc, desc
from datetime import datetime
from datetime import date
import requests
import os



task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")



@task_bp.route("", methods=["GET", "POST"])
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()
    if request.method == "GET":
        task_response = []

        for task in tasks:
            task_response.append({"id": task.task_id, 
                                "title": task.title, 
                                "description": task.description, 
                                "is_complete": task.is_complete()})
        return jsonify(task_response), 200
    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
        except KeyError:
            return make_response({"details": "Invalid data"}, 400)
        db.session.add(new_task)
        db.session.commit()
        update_new_task = new_task.to_json()
        update_new_task["is_complete"] = new_task.is_complete()


        return make_response({"task": update_new_task}, 201)

@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_single_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    if request.method == "GET":
        return {"task": task.to_json()}
    elif request.method == "PUT":
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]

        db.session.commit()
        updated_task = task.to_json()
        updated_task["is_complete"] = task.is_complete()

        return make_response({"task": updated_task}, 200)
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_with_completion(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    else: 
        local_date = date.today()
        today = local_date.strftime("%m%d%y")
        task.completed_at = today
        db.session.commit()
        updated_task = task.to_json()
        updated_task["is_complete"] = task.is_complete()
        token = os.environ.get("SLACK_BOT_TOKEN")
        completion_note = "Someone just completed the task " + str(task.title)
        message = {"channel": "task-notifications", "text": completion_note}
        auth = {"Authorization": token}
        slackbot_request = requests.post("https://slack.com/api/chat.postMessage", json=message,  headers=auth)



    return{"task": updated_task}


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_with_incomplete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    else: 
        updated_task = task.to_json()
        task.completed_at = None
        db.session.commit()
        updated_task["is_complete"] = task.is_complete()

    return {"task": updated_task}

@goal_bp.route("", methods=["POST", "GET"])
def create_or_get_goals():

    goals = Goal.query.all()
    if request.method == "GET":
        goal_response = []

        for goal in goals:
            goal_response.append({"id": goal.goal_id, 
                                "title": goal.title})
        return jsonify(goal_response), 200
    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_goal = Goal(title=request_body["title"])
        except KeyError:
            return make_response({"details": "Invalid data"}, 400)
        db.session.add(new_goal)
        db.session.commit()
    return make_response({"goal": new_goal.to_json()}, 201)

@goal_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_single_goal(goal_id): 
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    if request.method == "GET":
        return {"goal": goal.to_json()}
    elif request.method == "PUT":
        request_body = request.get_json()
        goal.title = request_body["title"]
        db.session.commit()
        return make_response({"goal": goal.to_json()}, 200)
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return make_response({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)
