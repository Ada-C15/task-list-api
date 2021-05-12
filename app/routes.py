from flask import Blueprint
import flask_migrate
from app import db 
from app.models.task import Task 
from app.models.goal import Goal
from flask import request, Blueprint, make_response 
from flask import jsonify
from datetime import date
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@tasks_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def handle_task():
    if request.method == "GET":  
        query_param_value = request.args.get("sort")
        if query_param_value == "asc":
            tasks = Task.query.order_by(Task.title.asc())

        elif query_param_value == "desc":
            tasks = Task.query.order_by(Task.title.desc())

        else:
            tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            })
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        if "title" in request_body and "description" in request_body and "completed_at" in request_body:
            new_task = Task(title = request_body["title"], 
                        description = request_body["description"], 
                        completed_at = request_body["completed_at"])
            db.session.add(new_task)
            db.session.commit() 

            if new_task.completed_at == None:
                is_complete = False 
            else:
                is_complete = True 
            
            return {
                "task":{
                    "id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": is_complete
            }}, 201
        else:
            return {
                "details": "Invalid data"
            }, 400


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def task_by_id(task_id):
    task = Task.query.get(task_id)
    if request.method == "GET":
        if task:
            if task.goal_id:
                return {"task": task.to_json_goal_id()}
            else:
                return {
                    "task": {
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False}
            }, 200

        else:
            return (f"None", 404)
    elif request.method == "PUT":
        if task:
            request_body = request.get_json()
            task.title = request_body["title"]
            task.description = request_body["description"]
            task.completed_at = request_body["completed_at"]
            db.session.commit()
            if task.completed_at == None:
                is_complete = False 
            else:
                is_complete = True 
            
            return {
                "task":{
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": is_complete
            }}, 200

        else:
            return (f"None", 404)

    elif request.method == "DELETE":
        if task:
            db.session.delete(task)
            db.session.commit()
            return {
                "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
            }, 200
        else:
            return (f"None", 404)

    else:
        return (f"None", 404)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return "", 404

    task.completed_at = date.today()
    db.session.commit()
    call_slack(task)
    return {
        "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": True
}}, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = None
        db.session.commit()
        return {
            "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
    }}, 200

    else:
        return (f"None", 404)

def call_slack(task):
    key = os.environ.get("api_key")
    url = "https://slack.com/api/chat.postMessage"
    slack_str = f"Someone just completed the task {task.title}"
    requests.post(url, data = {"token": key, "channel": "building-a-robot", "text": slack_str})

@goals_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def handle_goals():
    if request.method == "GET":  
        query_param_value = request.args.get("sort")
        if query_param_value == "asc":
            goals = Goal.query.order_by(Goal.title.asc())

        elif query_param_value == "desc":
            goals = Goal.query.order_by(Goal.title.desc())

        else:
            goals = Goal.query.all()
        goals_response = []
        for goal in goals:
            goals_response.append({
                "id": goal.goal_id,
                "title": goal.title
            })
        return jsonify(goals_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        if "title" in request_body:
            new_goal = Goal(title = request_body["title"])
            db.session.add(new_goal)
            db.session.commit() 

            # if new_goal.completed_at == None:
            #     is_complete = False 
            # else:
            #     is_complete = True 
            
            return {
                "goal":{
                    "id": new_goal.goal_id,
                    "title": new_goal.title
            }}, 201
        else:
            return {
                "details": "Invalid data"
            }, 400


@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def goal_by_id(goal_id):
    goal = Goal.query.get(goal_id)
    if request.method == "GET":
        if goal:
            return {
                "goal": {
                "id": goal.goal_id,
                "title": goal.title
                }}, 200

        else:
            return (f"None", 404)
    elif request.method == "PUT":
        if goal:
            request_body = request.get_json()
            goal.title = request_body["title"]
            # goal.completed_at = request_body["completed_at"]
            db.session.commit()
            # if goal.completed_at == None:
            #     is_complete = False 
            # else:
            #     is_complete = True 
            
            return {
                "goal":{
                    "id": goal.goal_id,
                    "title": goal.title
            }}, 200

        else:
            return (f"None", 404)

    elif request.method == "DELETE":
        if goal:
            db.session.delete(goal)
            db.session.commit()
            return {
                "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
            }, 200
        else:
            return (f"None", 404)

    else:
        return (f"None", 404)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def post_task_into_goal(goal_id):
    goal = Goal.query.get(goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        # goals.tasks.append(task)
        task = Task.query.get(task_id)
        task.goal_id = goal.goal_id

    db.session.commit() 
    return make_response({"id": int(goal_id), "task_ids": request_body["task_ids"]})

@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def handle_task_in_goals(goal_id):
    goal = Goal.query.get(goal_id) 
    if not goal:
        return "", 404
        
    list_of_tasks = []

    for task in goal.tasks:
        list_of_tasks.append(task.to_json_goal_id())
    return jsonify(id = int(goal_id), title = goal.title, tasks = list_of_tasks), 200


    #append all tasks to list_of_tasks that are assosiated to that goal. id, title, and tasks of goal 

