from app import db
from flask import Blueprint
from flask import request
from flask import jsonify, make_response
from .models.task import Task
from .models.goal import Goal
from datetime import datetime
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#make a post request
@tasks_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({"details": "Invalid data"}, 400) 
    task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])
    
    


    db.session.add(task)
    db.session.commit()

    return make_response({"task": task.return_task_json()}, 201)

#get requests
@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    tasks = Task.query.all()
    sort_query = request.args.get("sort")
    if sort_query:
        if 'asc' in sort_query:
            tasks = Task.query.order_by(Task.title.asc())
        elif 'desc' in sort_query:
            tasks = Task.query.order_by(Task.title.desc())
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id" : task.task_id,
            "title" : task.title,
            "description": task.description,
            "is_complete":task.task_completed()
        })
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def get_single_task(task_id):
    task = Task.query.get(task_id)
    form_data = request.get_json()
    if task is None:
        return make_response("", 404)
    if request.method == "GET":
        return make_response({"task":task.return_task_json()})
    elif request.method == "PUT":        
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return make_response({"task": task.return_task_json()})
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)
    


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    task.completed_at = datetime.now()

    path = 'https://slack.com/api/chat.postMessage'
    # slack_token = os.environ.get("SLACK_BOT_TOKEN")

    query_dictionary= {
        "token" : os.environ.get("SLACK_BOT_TOKEN"),
        "channel" : "task-notifications",
        "text" : f"Someone just completed the task {task.title}"
    }
    requests.post(path, data = query_dictionary)
    
    db.session.commit()
    return make_response({"task": task.return_task_json()}, 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def task_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404) 
    task.completed_at = None
    return make_response({"task": task.return_task_json()}, 200)

@goals_bp.route("", methods=["POST"])
def create_goal():
    
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400) 

    goal = Goal(title=request_body["title"])
    
    


    db.session.add(goal)
    db.session.commit()

    return make_response(goal.goal_json(), 201)

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id" : goal.goal_id,
            "title" : goal.title
        })
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def get_single_goal(goal_id):
    goal = Goal.query.get(goal_id)
    form_data = request.get_json()
    if goal is None:
        return make_response("", 404)
    if request.method == "GET":
        return make_response(goal.goal_json())
    elif request.method == "PUT":
        form_data = request.get_json()
        goal.title = form_data["title"]
        db.session.commit()
        return make_response(goal.goal_json())
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return make_response({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def goals_and_tasks(goal_id):
    goal = Goal.query.get(goal_id)
    
    request_body = request.get_json()
    #for all these tasks, I want to get their task id
    for task_id in request_body["task_ids"]:
        #tasks = assign tasks_ids
        task = Task.query.get(task_id)
        #make relationship to goal_id 
        task.goal_id = goal.goal_id



    db.session.commit()
    return make_response({"id": goal.goal_id, "task_ids": request_body["task_ids"]}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goals(goal_id):
    goal = Goal.query.get(goal_id)
    #if no goal, 404
    if goal is None:
        return make_response("", 404)

    tasks = Task.query.filter_by(goal_id=goal_id)
    task_list = []
    for task in tasks:
        task_list.append(task.return_task_json())

    return make_response({"id": goal.goal_id, "title": goal.title, "tasks": task_list }, 200)

    #else, goal_id is assign to a variable
    #get by filter, goal_id, - tasks and save to varible
    #for no matching tasks, make a varible w empty list
    #use for loop to go over tasks, apend those tasks to list
    #make use of task helper function to append to empty list


