from app import db
import requests
from app.models.task import Task
from flask import request, Blueprint, make_response
from flask import jsonify
from .models.task import Task
from .models.goal import Goal
from datetime import datetime
from dotenv import load_dotenv
import re
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

"""
Helper functions
"""
def wrong_input(task_id):
    return {
            "message": f"Task ID {task_id} must be an integer"
        }

def slack_send_message(message):
    path = "https://slack.com/api/chat.postMessage"
    query_params = {
        "channel" : "task-notifications",
        "text" : message
        #"text" : f"Task {task.id} with title {task.title} has been marked as complete"
    }
    authorization = os.environ.get('SLACK_URI')
    headers = {
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.post(path, data=query_params, headers=headers)


"""
CRUD for Tasks
"""

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    #Reads the HTTP request boby with:
    request_body = request.get_json()
    if len(request_body) == 3:
        new_task = Task(title = request_body["title"], description = request_body["description"], completed_at = request_body["completed_at"] )
        
        db.session.add(new_task)
        db.session.commit()
        slack_send_message("A new task has been created")
        return {
            "task" : new_task.to_json()
        }, 201
        #return make_response(jsonify(new_task)), 201
    elif ("title" not in request_body) or ("description" not in request_body) or ("completed_at" not in request_body):
        response = {
            "details" : "Invalid data"
        }
        return make_response(response,400)


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    tasks_response = []

    query_param_value=request.args.get("sort")
    if query_param_value == "asc":
        tasks = Task.query.order_by(Task.title)
    elif query_param_value == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_one_task(task_id):
    if not(re.match("[0-9]",task_id)): 
        return make_response(wrong_input(task_id),400)

    task = Task.query.get(task_id)
    if task:
        return{
            "task" : task.to_json()
        } , 200
    return make_response("",404)


@tasks_bp.route("/<task_id>",methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    if not(re.match("[0-9]",task_id)): 
        return make_response(wrong_input(task_id),400)

    task = Task.query.get(task_id)
    if task is None:
        return make_response("",404)

    updates_body = request.get_json()
    task.title = updates_body["title"]
    task.description = updates_body["description"]
    task.completed_at = updates_body["completed_at"]

    db.session.commit()
    slack_send_message(f"Task {task_id} has been successfully updated")
    return {
            "task" : task.to_json()
    }, 200

@tasks_bp.route("/<task_id>",methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    if not(re.match("[0-9]",task_id)): 
        return make_response(wrong_input(task_id),400)
    
    task = Task.query.get(task_id)
    if task is None:
        return make_response("",404)

    db.session.delete(task)
    db.session.commit()
    slack_send_message(f"Task {task_id} has been successfully deleted")
    return {
        "details" : f"Task {task.id} \"{task.title}\" successfully deleted"
    }, 200


@tasks_bp.route("/<task_id>/<complete_status>",methods=["PATCH"], strict_slashes=False)
def mark_status_task(task_id, complete_status):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("",404)
    
    if complete_status == "mark_complete":
        completed_date = datetime.today()
        task.completed_at = completed_date
        slack_send_message(f"Task {task_id} has been marked as complete")
        print("I made it to this point")
    else:
        task.completed_at = None
    
    db.session.commit()

    return {
            "task" : task.to_json()
    }, 200



"""
CRUD for Goals
"""

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    #Reads the HTTP request boby with:
    request_body = request.get_json()
    
    if "title" not in request_body:
        response = {
            "details" : "Invalid data"
        }
        return make_response(response,400)
    new_goal = Goal(title = request_body["title"])

    db.session.add(new_goal)
    db.session.commit()
    slack_send_message("A new goal has been created")

    return {
        "goal" : new_goal.to_json()
    }, 201


@goals_bp.route("<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def create_task_ids_to_goal(goal_id):
    request_body = request.get_json()
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("",404)
    
    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.g_id = goal.g_id
    
    db.session.commit()

    response = {
        "id" : goal.g_id,
        "task_ids": request_body["task_ids"]
    }
    return jsonify(response), 200


@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_goal():
    goals_response = []
    goals = Goal.query.all()

    for goal in goals:
        goals_response.append(goal.to_json())
    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def get_one_goal(goal_id):
    if not(re.match("[0-9]",goal_id)): 
        return {
            "message": f"Goal ID {goal_id} must be an integer"
        }, 400

    goal = Goal.query.get(goal_id)
    if goal:
        return{
            "goal" : goal.to_json()
        } , 200
    return make_response("",404)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_tasks_for_one_goal(goal_id):
    if not(re.match("[0-9]",goal_id)): 
        return {
            "message": f"Goal ID {goal_id} must be an integer"
        }, 400

    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("",404)
    
    #tasks = Task.query.filter_by(g_id=goal.g_id)
    tasks = goal.tasks
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    response = {
        "id": goal.g_id,
        "title": goal.title,
        "tasks": tasks_response
    }
    return jsonify(response), 200



@goals_bp.route("/<goal_id>",methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):
    if not(re.match("[0-9]",goal_id)): 
        return {
            "message": f"Goal ID {goal_id} must be an integer"
        }, 400

    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("",404)

    updates_body = request.get_json()
    goal.title = updates_body["title"]

    db.session.commit()
    slack_send_message(f"Goal {goal_id} has been successfully updated")
    return {
            "goal" : goal.to_json()
    }, 200



@goals_bp.route("/<goal_id>",methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):
    if not(re.match("[0-9]",goal_id)): 
        return {
            "message": f"Goal ID {goal_id} must be an integer"
        }, 400
    
    goal = Goal.query.get(goal_id)
    if goal == None:
        return make_response("",404)

    db.session.delete(goal)
    db.session.commit()
    slack_send_message(f"Goal {goal_id} has been successfully deleted")
    return {
        "details" : f"Goal {goal.g_id} \"{goal.title}\" successfully deleted"
    }, 200
