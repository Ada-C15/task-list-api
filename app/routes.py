from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response
from flask import jsonify
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os 
 




tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")



# GET AND CREATE TASK ITEMS
@tasks_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def tasks():
    
    if request.method == "GET":
        task_order = request.args.get("sort")
        if task_order == None:
            tasks = Task.query.all() # get all items in list
        elif task_order == "asc": #to sort by ascending 
            tasks = Task.query.order_by(asc(Task.title))
        elif task_order == "desc": #to sort by descending 
            tasks = Task.query.order_by(desc(Task.title))

        tasks_response = []
        for task in tasks:
            tasks_response.append(task.display_tasks())
        return jsonify(tasks_response)

    
    else:
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)
            
        task = Task(title = request_body["title"],
                            description = request_body["description"],
                            completed_at = request_body["completed_at"])
        

        db.session.add(task)
        db.session.commit()



        return jsonify({"task": task.display_tasks()}), 201      

# GET, CHANGE, AND DELETE A SPECIFIC TASK ID
@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        return jsonify({"task": task.display_tasks()}), 200

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return jsonify({"task": task.display_tasks()}), 200


    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": (f'Task {task.id} "{task.title}" successfully deleted')}), 200
    
    
    return {
        "message": f"Task with id {task.id} was not found",
        "success": False,
    }, 404



# MARK ID AS COMPLETE  
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def complete_task(task_id):

    if request.method == "PATCH":
        task = Task.query.get(task_id)
        if task is None:
            return jsonify(None), 404

        task.completed_at = datetime.now()
        db.session.commit()
        slack_message(task)
        return jsonify({"task": task.display_tasks()}), 200

# SEND MESSAGE TO SLACK WHEN COMPLETE
def slack_message(task):

    slack_token = os.environ.get("TOKEN")
    
    url = "https://slack.com/api/chat.postMessage?channel=task-notifications"

    payload = {"text": f"Someone just completed the task: '{task.title}'!"}
    headers = {"Authorization": f"Bearer {slack_token}"}

    return requests.request("PATCH", url, headers=headers, data=payload)


# MARK ID AS INCOMPLETE 
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def incomplete_task(task_id):

        if request.method == "PATCH":
            task = Task.query.get(task_id)
            if task is None:
                return jsonify(None), 404

            task.completed_at = None

            return jsonify({"task": task.display_tasks()}), 200



    
# GET AND CREATE GOAL ITEMS
@goals_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def one_goal():
    
    if request.method == "GET":
        goals = Goal.query.all() # get all items in goal list
        
        goals_response = []

        for goal in goals:
            goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
            })

        return jsonify(goals_response)

    
    if request.method == "POST":
        request_body = request.get_json()
        if ("title" not in request_body):
            return make_response(jsonify({"details": "Invalid data"}), 400)
        else:
            goal = Goal(title = request_body["title"])
        

        db.session.add(goal)
        db.session.commit()


        return make_response({"goal": {
            "id": goal.goal_id,
            "title": goal.title
            }}, 201)





# # GET, CHANGE, AND DELETE A SPECIFIC GOAL ID
@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    if request.method == "GET":
        return make_response({"goal": {
            "id": goal.goal_id,
            "title": goal.title
            }}, 200)

    elif request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data["title"]
        

        db.session.commit()

        return make_response({"goal": {
            "id": goal.goal_id,
            "title": goal.title
            }}, 200)


    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return jsonify({"details": (f'Goal {goal.goal_id} "{goal.title}" successfully deleted')}), 200
    
    
    return {
        "message": f"Goal with id {goal.goal_id} was not found",
        "success": False,
    }, 404
