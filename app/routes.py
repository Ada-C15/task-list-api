from flask import Blueprint, request, jsonify
from werkzeug.wrappers import PlainRequest
from app import db
from flask.helpers import make_response
from app.models.task import Task
from app.models.goal import Goal
from datetime import date
import os
import requests

# sets up blueprints - with details
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# 
# Wave 1: GET & POST functions - gets data for all tasks in table, and creates new tasks
# come back and refactor into task_index & independent POST function
@tasks_bp.route("", methods=["GET","POST"], strict_slashes=False)
def handle_tasks():
    if request.method == "GET":
        task_title_from_url = request.args.get("title")
        # search for task by title
        if task_title_from_url:
            tasks = Task.query.filter_by(title=task_title_from_url)
        # all tasks
        else:
            tasks = Task.query.all()
    
        tasks_response = []

        for task in tasks:
            tasks_response.append(task.to_json())

        # Wave 2 ascending/descending logic for GET method
        if "asc" in request.full_path:
            sorted_ascending = sorted(tasks_response, key=lambda x: x.get("title"))
            return jsonify(sorted_ascending)
        
        elif "desc" in request.full_path:
            sorted_descending = sorted(tasks_response, key=lambda x: x.get("title"), reverse=True)
            return jsonify(sorted_descending)

        return jsonify(tasks_response), 200

    elif request.method == "POST":
        # try and except block for KeyError
        try:
            request_body = request.get_json()

            new_task = Task(title=request_body["title"],
                            description=request_body["description"],
                            completed_at=request_body["completed_at"]
                            )

            db.session.add(new_task)
            db.session.commit()

            return {
                "task": new_task.to_json()
            }, 201
        
        except KeyError:
            return{"details": "Invalid data"}, 400

# helper function that will eventually check for task_ids being integers
def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

# GET function - gets the data for the task with the specified task_id
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_one_task(task_id):
    if not is_int(task_id):
        return{
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    else:
        return {
            "task": task.to_json()
        }, 200
# PUT function - Updates either/or both title & description data 
# for specified task (via task_id)
@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):

    task = Task.query.get(task_id)

    if task:
        task_data = request.get_json()

        task.title = task_data["title"]
        task.description = task_data["description"]

        db.session.commit()

        return{
            "task": task.to_json()
        }, 200
    else:
        return make_response("", 404)

# DELETE function - deletes specified task (via task_id)
@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    else:
        db.session.delete(task)
        db.session.commit()

        return {
            "details": f'Task {task.task_id} "{task.title}" successfully deleted'
        }

# PATCH function - mark complete (includes call_slack_bot helper funciton)
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    else:
        task.completed_at = date.today()
        db.session.commit()

        call_slack_bot(task)

        return{
            "task": task.to_json()
        }, 200

# PATCH function - mark_incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):

    task= Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    else:
        task.completed_at = None
        db.session.commit()

        return {
            "task": task.to_json()
        }, 200

# Wave 4: separate function that sends a POST request to the slack bot
def call_slack_bot(task):
    SLACK_API_TOKEN = os.environ.get('BOT_API_TOKEN')
    url = "https://slack.com/api/chat.postMessage"
    payload = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    headers = {
        "Authorization": f"Bearer {SLACK_API_TOKEN}",
    }
    return requests.request("POST", url, data=payload, headers=headers)

# wave 5 goal routes
# refactor into separate GET & POST functions
@goals_bp.route("", methods=["GET","POST"], strict_slashes=False)
def handle_goals():
    if request.method == "GET":
        goal_title_from_url = request.args.get("title")
        # search for goal by title
        if goal_title_from_url:
            goals = Goal.query.filter_by(title=goal_title_from_url)
        # all goals
        else:
            goals = Goal.query.all()
    
        goals_response = []

        for goal in goals:
            goals_response.append(goal.goal_json())
        
        # implements Wave 2 ascending/descending sort logic
        if "asc" in request.full_path:
            sorted_ascending = sorted(goals_response, key=lambda x: x.get("title"))
            return jsonify(sorted_ascending)
        
        elif "desc" in request.full_path:
            sorted_descending = sorted(goals_response, key=lambda x: x.get("title"), reverse=True)
            return jsonify(sorted_descending)

        return jsonify(goals_response), 200

    elif request.method == "POST":
        # try and except block for KeyError
        try:
            request_body = request.get_json()

            new_goal = Goal(title=request_body["title"])

            db.session.add(new_goal)
            db.session.commit()

            return {
                "goal": new_goal.goal_json()
            }, 201
        
        except KeyError:
            return{"details": "Invalid data"}, 400

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

# Handles GET requests for 1 method with the provided goal id. 
@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def get_one_goal(goal_id):
    if not is_int(goal_id):
        return{
            "message": f"ID {goal_id} must be an integer",
            "success": False
        }, 400
    
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)
    else:
        return {
            "goal": goal.goal_json()
        }, 200

@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal:
        goal_data = request.get_json()

        goal.title = goal_data["title"]

        db.session.commit()

        return{
            "goal": goal.goal_json()
        }, 200
    else:
        return make_response("", 404)

@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)
    else:
        db.session.delete(goal)
        db.session.commit()

        return {
            "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
        }
# wave 6
# POST function: one(goal)-to-many(tasks) relationship
@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def post_goal_tasks(goal_id):
    # gets the passed in information and gives it in json format
    request_body = request.get_json()
    # gets the goal that is associated with the given goal_id
    goal = Goal.query.get(goal_id)

    # if no goal with the provided goal_id, returns a 404 error
    if not goal:
        return make_response("", 404)
    else:
        # iterates through the values for the "task_id" keys in request_body
        for task_id in request_body["task_ids"]:
            # in each iteration, gets the task that corresponds to the current task_id
            task = Task.query.get(task_id)
            # sets the value in the goaltask_id foreignkey column (in task table) to the corresponding goal_id
            task.goaltask_id = goal_id
            # commits the addition to the table to the database
            db.session.commit()
    # when a POST request is sent, return this in the response body
    return {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

# GET function: one(goal)-to-many(tasks)
@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_goal_tasks(goal_id):
    request_body = request.get_json()
    goal = Goal.query.get(goal_id)
    # sets task variable equal to the task with the corresponding goal (in foreignkey column)
    task = Task.query.get(goal_id)

    # if goal doesn't exist, return a 404 error
    if not goal:
        return make_response("", 404)
    else:
        # sets outer dictionary (named response_dict) to dictionary created in Goal
        response_dict = goal.goal_json()
        # if there are no tasks associated with the goal, sets "tasks" equal to empty list
        if task == None:
            response_dict["tasks"] = []
        else:
            # if task(s) associated with goal, return the task.json() 
            # data pulled from Task function
            task_data_dict = task.to_json()
            # sets response_dict "tasks"  & task_data_dict "goal_id" values
            response_dict["tasks"] = [response_dict]
            task_data_dict["goal_id"] = goal.goal_id
        
        # commit changes to tables
        db.session.commit()
        return make_response(response_dict, 200)