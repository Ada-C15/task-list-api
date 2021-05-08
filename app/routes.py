from flask import Blueprint 
from flask import request
from flask import jsonify 
from flask import make_response
from app.models.task import Task
from app.models.goal import Goal
from app import db 
from datetime import datetime
import os
import time
from slack import WebClient

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


#wave_1
@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    if not "title" in request_body or not "description" in request_body or not "completed_at" in request_body:
        return jsonify(
                {"details": "Invalid data"}
                ), 400
    else: 
        task = Task(title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"])

    db.session.add(task)
    db.session.commit()

    return {
            "task": task.to_json()
        }, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    #sort title by ace and desc order
    #check wave_2 tests
    sort_by_title = request.args.get("sort")
    if sort_by_title == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_by_title == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response)


#GET PUT DELETE 
@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    elif request.method == "GET":
        return make_response({"task": task.to_json()}, 200)

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return make_response(
            {"task": task.to_json()
        }, 200)

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
            })

#wave_3 
#creating custom endpoints with is_complete: True or False
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"]) #update
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if not task:
        return ("", 404)

    task.completed_at = datetime.now()

    db.session.commit()

    message_to_slack("#task-notifications", f"Someone just completed the task {task.title}")
    return {
        "task": task.to_json()
    }, 200

# Slack API - lets send some messages from here 

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"]) #update
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return ("", 404)

    if task.completed_at != None:
        task.completed_at = None
    
    db.session.commit()

    message_to_slack("#task-notifications", f"Someone just completed the task {task.title}")
    return {
        "task": task.to_json()
        }, 200

#wave 4 
client = WebClient(token=os.environ["SLACK_API_TOKEN"])

# wrapper for sending a Slack message
def message_to_slack(channel, message):
    return client.chat_postMessage(
        channel=channel,
        text=message
    )


#wave_5
# created second models for goals
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return (
            {"details": "Invalid data"}
            ), 400
    else:
        add_goal = Goal(title = request_body["title"])

        db.session.add(add_goal)
        db.session.commit()

        return make_response({
                "goal": add_goal.to_json_goal()
            }, 201)

@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals: 
        goals_response.append(goal.to_json_goal())

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_goals(goal_id):

    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    
    if request.method == "GET":
        return make_response(
            {"goal": goal.to_json_goal()
        }, 200)

    elif request.method == "PUT":
        form_data = request.get_json()
        goal.title = form_data["title"]

        db.session.commit()

        return make_response(
            {"goal": goal.to_json_goal()}, 200)

    elif request.method == "DELETE":

        db.session.delete(goal)
        db.session.commit()

        return make_response({
            "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
            })











# Wave 6
# Establishing a One-to-Many Relationship

#optional- deployment

#enhancements




