from flask.wrappers import Response
import requests
import os
from app import db
from .models.task import Task
from flask import Blueprint, make_response, request, jsonify
from datetime import datetime
from dotenv import load_dotenv
from .models.goal import Goal

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():     
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return {
                "details": "Invalid data"
            }, 400
    
        new_task = Task(title=request_body['title'], 
                        description=request_body['description'],
                        completed_at=request_body['completed_at'])
        
        db.session.add(new_task)
        db.session.commit()
        response_body = {
            "task": new_task.resp_json()
        }
        return jsonify(response_body), 201

    elif request.method == "GET":
        sorting_tasks = request.args.get("sort")
        
        tasks = Task.query.all()
        tasks_response = []

        if sorting_tasks == "asc":
            asc_order = Task.query.order_by(Task.title.asc())
            new_order = []
        
            for task in asc_order:
               new_order.append(task.resp_json())
            return jsonify(new_order), 200

        elif sorting_tasks == "desc":
            desc_order = Task.query.order_by(Task.title.desc())
            new_order = []
        
            for task in desc_order:
               new_order.append(task.resp_json())
            return jsonify(new_order), 200


        for task in tasks:
            tasks_response.append(task.resp_json())

        return jsonify(tasks_response), 200




    
        
@tasks_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def handle_task(id):
    task = Task.query.get(id)

    if task is None: 
        return  make_response("", 404)
    if request.method == "GET":
        response_body = {
                "task": task.resp_json()
            }
        return jsonify(response_body), 200

    elif request.method == "PUT":

        request_body = request.get_json()
    
        task.title=request_body['title'], 
        task.description=request_body['description'],
        task.completed_at=request_body['completed_at']
        
        db.session.add(task)
        db.session.commit()

        response_body = {
                "task": task.resp_json()
            }
        return jsonify(response_body), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        
        return {
            "details": f"Task {task.id} \"{task.title}\" successfully deleted"
        }, 200

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])

def task_completed(id):
    task = Task.query.get(id)

    if task is None:
        return make_response("", 404)
    
    task.completed_at = datetime.now()
    db.session.commit()
    response_body = {
            "task": task.resp_json()
        }
    send_to_slack(task)
    return make_response(response_body, 200)


def send_to_slack(task):
    path = "https://api.slack.com/methods/chat.postMessage"
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
    slack_response = f"Someone just completed the task{task.title}"
    query_params = {
        "channel": "task-notifications",
        "text": slack_response
    }
    header = {
            "Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"
        }
    response = requests.post(path, params=query_params, headers=header)

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])

def task_incomplete(id):
    task = Task.query.get(id)

    if task is None:
        return make_response("", 404)
    
    task.completed_at = None
    db.session.commit()

    response_body = {
            "task": task.resp_json()
        }
    return jsonify(response_body), 200


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST", "GET"])
def handle_goals():     
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return {
                "details": "Invalid data"
            }, 400
    
        new_goal = Goal(title=request_body['title'])

        db.session.add(new_goal)
        db.session.commit()

        response_body = {
            "goal": new_goal.json_2()
        }
        return jsonify(response_body), 201

    elif request.method == "GET":
        
        goals = Goal.query.all()
        goals_response = []

        for goal in goals:
            goals_response.append(goal.json_2())

        return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_goal_id(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)
    if request.method =="GET":
        
        return {
        "goal": goal.json_2()
        }, 200

    elif request.method =="PUT":
        request_body = request.get_json()
        goal.title = request_body["title"]
        db.session.commit()

        return {
        "goal": goal.json_2()
        }, 200

    elif request.method =="DELETE":
        db.session.delete(goal)
        db.session.commit()
        return {
            "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        }, 200
#   ******* wave 6 *******
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def handle_tasks_and_goal(goal_id):
    goal_id = int(goal_id)
    if goal_id is None:
        return make_response("", 404)

    request_body = request.get_json()
    new_task_ids = request_body["task_ids"]
    list_new_ids = []

    for task_id in new_task_ids:
        some_task = Task.query.get(task_id)
        some_task.goal_id = goal_id
        list_new_ids.append(task_id)
        db.session.commit()

    return make_response({
        "id": goal_id ,
        "task_ids": new_task_ids
        }, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def handle_all_things(goal_id):
    tasks_info = []
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)


    all_tasks = Task.query.all()

    for task in all_tasks:
        tasks_info.append(task.resp_json())

    return make_response({
        "id": int(goal_id),
        "title": goal.title,
        "tasks": tasks_info
    }, 200)

