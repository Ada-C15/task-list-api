# from werkzeug.wrappers import ETagRequestMixin
from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET","POST"])
def handle_tasks():
    if request.method == "GET":
        sort = request.args.get("sort")

        if sort == "asc":
            tasks = Task.query.order_by(asc("title"))
        
        elif sort == "desc":
            tasks = Task.query.order_by(desc("title"))
        
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
            })
        return jsonify(tasks_response)

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body.keys() or "description" not in request_body.keys() or "completed_at" not in request_body.keys():
            return make_response({"details": "Invalid data"}, 400)

        else:    
            new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
            
            db.session.add(new_task)
            db.session.commit()

            return make_response({"task": new_task.make_json()}, 201)

@tasks_bp.route("/<task_id>", methods= ["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    elif request.method == "GET":
        return make_response({"task": task.make_json()})

    elif request.method == "PUT":
        request_body = request.get_json()

        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]

        db.session.commit()

        return make_response({"task": task.make_json()}) 
        
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        return {
            "details": (f"Task {task.task_id} \"{task.title}\" successfully deleted")
        }

@tasks_bp.route("/<task_id>/mark_complete", methods= ["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response("", 404)

    API_KEY = os.environ.get("API_KEY")
    PATH = "https://slack.com/api/chat.postMessage"
    query_params = {
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}."
        }
    task.completed_at = datetime.utcnow()
    db.session.commit()
    requests.post(PATH, data=query_params, headers={"Authorization":API_KEY})
    return make_response({"task": task.make_json()}) 

@tasks_bp.route("/<task_id>/mark_incomplete", methods= ["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response("", 404)

    task.completed_at = None
    db.session.commit()
    return make_response({"task": task.make_json()}) 

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET","POST"])
def handle_goals():
    if request.method == "GET":
        goals = Goal.query.all()

        goal_response = []
        for goal in goals:
            goal_response.append({
                "id": goal.goal_id,
                "title": goal.title,
            })
        return jsonify(goal_response)

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body.keys():
            return make_response({"details": "Invalid data"}, 400)
        
        else:
            new_goal = Goal(title=request_body["title"])

            db.session.add(new_goal)
            db.session.commit()

            return make_response({"goal": new_goal.create_response()}, 201)

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal == None:
        return make_response("", 404)
    
    elif request.method == "GET":
        return make_response({"goal": goal.create_response()})
    
    elif request.method == "PUT":
        request_body = request.get_json()

        goal.title = request_body["title"]

        db.session.commit()

        return make_response({"goal": goal.create_response()})
    
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()

        return {"details": (f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted")}


@goals_bp.route("/<goal_id>/tasks", methods=["GET", "POST"])
def handle_goal_tasks(goal_id):
    goal = Goal.query.get(goal_id)

    if goal == None:
        return make_response("", 404)
    
    elif request.method == "GET":
        # tasks_list = Task.query.get(goal_id)
        return make_response(goal.return_goal_tasks())

        # return make_response({
        #     "id": goal.goal_id,
        #     "title": goal.title,
        #     "tasks": tasks_list
        # })
    
    elif request.method == "POST":
        request_body = request.get_json()
        task_ids = request_body["task_ids"]

        for id in task_ids:
            task = Task.query.get(id)
            task.goal_id = goal.goal_id
        
        db.session.commit()

        return make_response(jsonify({"id": goal.goal_id, "task_ids": task_ids}))