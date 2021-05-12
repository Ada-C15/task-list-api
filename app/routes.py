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

# Loads the SLACKBOT_TOKEN and TASK_NOTIFICATIONS_CHANNEL_ID from our .env file so that the os module is able to see it: 
load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
# relation_bp = Blueprint("est_relation", __name__, url_prefix="/goals")

#=============================================================================

def slack_post_to_task_notifications_channel(text):
    """
    inputs: text (string), the message to be posted
    outputs: a message posted to the task-notifications channel in Slack
    """
    # Reads the value of the environment variable SLACKBOT_TOKEN and assigns it to "Authorization" key in headers 
    post_headers = {"Authorization": os.environ.get("SLACKBOT_TOKEN")}
    
    post_data = {
        "channel": os.environ.get("TASK_NOTIFICATIONS_CHANNEL_ID"),
        "text": text
    }

    requests.post('https://slack.com/api/chat.postMessage', headers=post_headers, data=post_data)



def is_int(input_id):
    """
    input: the input id value
    output: tries to return an integer form of input value; if that raises an error, it returns False
    """
    try:
        return int(input_id)
    except ValueError:
        return False



#=============================================================================
    
# Get One Saved Task (Successful = Returns 200 OK); No Matching Task Returns 404 Not Found
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):

    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    saved_task = Task.query.get_or_404(task_id)

    return make_response({"task":(saved_task.convert_to_json())}, 200)

# Update One Task (Successful = Returns 200 OK); No Matching Task Returns 404 Not Found
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    # Check for valid id
    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    saved_task = Task.query.get_or_404(task_id)
    
    form_data = request.get_json()

    saved_task.title = form_data["title"]
    saved_task.description = form_data["description"]
    saved_task.completed_at = form_data["completed_at"]

    db.session.commit()

    return make_response({"task":(saved_task.convert_to_json())}, 200)

# Delete One Task (Successful = Returns 200 OK); No Matching Task Returns 404 Not Found
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    # Check for valid id
    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    saved_task = Task.query.get_or_404(task_id)

    db.session.delete(saved_task)
    db.session.commit()
    return {"details": f"Task {saved_task.task_id} \"{saved_task.title}\" successfully deleted"}, 200

# Allows client to send a patch request to mark a task as complete or incomplete (Successful = Returns 200 OK); No Matching Task Returns 404 Not Found
@tasks_bp.route("/<task_id>/<toggle_action>", methods=["PATCH"])
def toggle_task_complete(task_id, toggle_action):

    # Check for valid id
    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

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

# Get All Saved Tasks (Successful = Returns 200 OK); No Saved Tasks still returns 200 OK
@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def task_index():

    # Gets query param sorting direction from query key "sort" and assigns to a variable
    query_sort_direction = request.args.get("sort")
    tasks_response = []

    # Queries a list of all Task instances in ascending order by title
    if query_sort_direction == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    
    # Queries a list of all Task instances in descending order by title
    elif query_sort_direction == "desc": 
        tasks = Task.query.order_by(desc(Task.title))

    # If no query param "sort" key is passed in, just queries a list of all Task instances, which defaults to ascending order by ID number 
    else:
        tasks = Task.query.all()

    # Converts each task dictionary to JSON and appends to tasks_response list 
    for task in tasks:
        tasks_response.append(task.convert_to_json())

    # Converts tasks_response list into a JSON response object, returns it
    return jsonify(tasks_response), 200

# Create Valid Task With null completed_at (Successful = Returns 201); Attempt to create Invalid Task With Missing Data Returns 400 Bad Request
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

    if not is_int(goal_id):
        return {
            "message": f"ID {goal_id} must be an integer",
            "success": False
        }, 400

    saved_goal = Goal.query.get_or_404(goal_id)

    return make_response({"goal":(saved_goal.convert_to_json())}, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    if not is_int(goal_id):
        return {
            "message": f"ID {goal_id} must be an integer",
            "success": False
        }, 400

    saved_goal = Goal.query.get_or_404(goal_id)
    
    form_data = request.get_json()

    saved_goal.title = form_data["title"]

    db.session.commit()

    return make_response({"goal":(saved_goal.convert_to_json())}, 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):

    if not is_int(goal_id):
        return {
            "message": f"ID {goal_id} must be an integer",
            "success": False
        }, 400

    saved_goal = Goal.query.get_or_404(goal_id)

    db.session.delete(saved_goal)
    db.session.commit()
    return {"details": f"Goal {saved_goal.goal_id} \"{saved_goal.title}\" successfully deleted"}, 200

#=========================================================================

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def task_ids_to_goal(goal_id):

    saved_goal = Goal.query.get_or_404(goal_id)

    form_data = request.get_json()

    for each_task_id in form_data["task_ids"]:
        updated_task = Task.query.get_or_404(each_task_id)
        updated_task.matching_goal_id = saved_goal.goal_id

    db.session.commit()

    return make_response({"test"}, 200)












