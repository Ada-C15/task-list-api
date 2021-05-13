import datetime
import requests
from flask.wrappers import Response 
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import asc, desc
from flask import request, Blueprint, make_response, jsonify
from dotenv import load_dotenv
import os


load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


# HELPER FUNCTIONS:
#=============================================================================

def slack_post_to_task_notifications_channel(text):
    """
    inputs: text (string), which is the message to be posted
    outputs: a message posted to the task-notifications channel in Slack
    """
    post_headers = {"Authorization": os.environ.get("SLACKBOT_TOKEN")}
    
    post_data = {
        "channel": os.environ.get("TASK_NOTIFICATIONS_CHANNEL_ID"),
        "text": text
    }

    requests.post('https://slack.com/api/chat.postMessage', headers=post_headers, data=post_data)

def is_int(value):
    """
    input: any value
    output: tries to return an integer form of input value; if that raises an error, it returns False
    """
    try:
        return int(value)
    except ValueError:
        return False

def valid_id_or_400(input_id):
    """
    input: an input ID 
    output: returns False and a 400 status code if the input ID is not an integer 
    """

    if not is_int(input_id):
        return {
            "message": f"ID {input_id} must be an integer",
            "success": False
        }, 400
    

# TASK ENDPOINTS:
#=============================================================================
    
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):

    valid_id_or_400(task_id)

    saved_task = Task.query.get_or_404(task_id)

    return make_response({"task":(saved_task.convert_to_json())}, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    valid_id_or_400(task_id)

    saved_task = Task.query.get_or_404(task_id)
    
    form_data = request.get_json()

    saved_task.title = form_data["title"]
    saved_task.description = form_data["description"]
    saved_task.completed_at = form_data["completed_at"]

    db.session.commit()

    return make_response({"task":(saved_task.convert_to_json())}, 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    valid_id_or_400(task_id)

    saved_task = Task.query.get_or_404(task_id)

    db.session.delete(saved_task)
    db.session.commit()
    return {"details": f"Task {saved_task.task_id} \"{saved_task.title}\" successfully deleted"}, 200


@tasks_bp.route("/<task_id>/<toggle_action>", methods=["PATCH"])
def toggle_task_complete(task_id, toggle_action):

    valid_id_or_400(task_id)

    saved_task = Task.query.get_or_404(task_id)

    if toggle_action == "mark_complete":
        # Updates saved_task "completed_at" attribute with current time, in date-time format 
        saved_task.completed_at = datetime.datetime.now()
        db.session.commit()

        slack_post_to_task_notifications_channel(f"Someone just completed the task {saved_task.title}")

    elif toggle_action == "mark_incomplete":
        saved_task.completed_at = None
        db.session.commit()

    return make_response({"task":(saved_task.convert_to_json())}, 200)


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def task_index():

    query_sort_direction = request.args.get("sort")
    tasks_response = []

    if query_sort_direction == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif query_sort_direction == "desc": 
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(task.convert_to_json())

    return jsonify(tasks_response), 200


@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():

    request_body = request.get_json()

    if (not request_body) or ("description" not in request_body) or ("title" not in request_body) or ("completed_at" not in request_body):
        return { "details": "Invalid data"
        }, 400

    new_task = Task(title=request_body["title"],
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":(new_task.convert_to_json())}, 201)


# GOAL ENDPOINTS:
#=============================================================================

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():

    request_body = request.get_json()

    if (not request_body) or ("title" not in request_body):
        return { "details": "Invalid data"
        }, 400

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal":(new_goal.convert_to_json())}, 201)
    

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def goal_index():

    query_sort_direction = request.args.get("sort")
    goals_response = []

    if query_sort_direction == "asc":
        goals = Goal.query.order_by(asc(Goal.title))
    elif query_sort_direction == "desc": 
        goals = Goal.query.order_by(desc(Goal.title))
    else:
        goals = Goal.query.all()

    for goal in goals:
        goals_response.append(goal.convert_to_json())

    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def get_single_goal(goal_id):

    valid_id_or_400(goal_id)

    saved_goal = Goal.query.get_or_404(goal_id)

    return make_response({"goal":(saved_goal.convert_to_json())}, 200)


@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):

    valid_id_or_400(goal_id)

    saved_goal = Goal.query.get_or_404(goal_id)
    
    form_data = request.get_json()

    saved_goal.title = form_data["title"]

    db.session.commit()

    return make_response({"goal":(saved_goal.convert_to_json())}, 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):

    valid_id_or_400(goal_id)

    saved_goal = Goal.query.get_or_404(goal_id)

    db.session.delete(saved_goal)
    db.session.commit()
    return {"details": f"Goal {saved_goal.goal_id} \"{saved_goal.title}\" successfully deleted"}, 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def post_tasks_to_goal(goal_id):

    valid_id_or_400(goal_id)

    saved_goal = Goal.query.get_or_404(goal_id)

    form_data = request.get_json()
    task_ids = form_data["task_ids"]

    for each_task_id in task_ids:
        updated_task = Task.query.get_or_404(each_task_id)
        updated_task.match_goal_id = saved_goal.goal_id

    db.session.commit()

    return make_response({"id": saved_goal.goal_id, "task_ids": task_ids}, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_tasks_for_goal(goal_id):

    valid_id_or_400(goal_id)

    saved_goal = Goal.query.get_or_404(goal_id)
    saved_goal_tasks = []

    tasks = Task.query.filter_by(match_goal_id=goal_id)

    for task in tasks:
        saved_goal_tasks.append(task.convert_to_json())

    response_body = saved_goal.convert_to_json(saved_goal_tasks)

    return make_response(response_body, 200)

    
    











