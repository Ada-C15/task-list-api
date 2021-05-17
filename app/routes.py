# datetime is a Python module - use to work with dates as date objects
import datetime
# the Python requests library is the de facto standard for formatting HTTP requests in Python, which you use in conjuction with a request method a la requests.get() or requests.post()
import requests
#  Response is a Flask class that represents HTTP responses - note that make_response() actually uses Response internally
from flask.wrappers import Response 
# need to import db module in order to add and commit (save) to databases when requests get made to add or update database items
from app import db
# Both models need to be imported to use them to link code to their respective databases (a Model is just a class inherited from the db.Model)
from app.models.task import Task
from app.models.goal import Goal
# asc and desc are module functions that need to be imported to be used
from sqlalchemy import asc, desc
# The following are all dependencies:
# request is an OBJECT (not to be confused with the 'requests' PACKAGE) used to get info about an HTTP request
# Blueprint is a class 
#  ❓ make_response is a Flask helper method that instantiates a Response object - I'm a little confused about what I need this, as the code seems to work without it. But I know that it convert the return value from a view function to an instance of response_class. (from Flask documentation)
# jsonify is a method used to convert a JSON HTTP request body into a Python dictionary 
from flask import request, Blueprint, make_response, jsonify
# dotenv is a Python package 
from dotenv import load_dotenv
# os is a module that provides the ability to read environmental variables, which are actually stored outside of the code - needed to be able to read the hidden bot API token
import os

from flask import abort

# this method loads the values from the .env file which the os module can then read 
load_dotenv()

# instantiating blueprints for task and goal
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


# HELPER FUNCTIONS:
#=============================================================================

def slack_post_to_task_notifications_channel(text):
    """
    inputs: text (string), which is the message to be posted
    outputs: a message posted to the task-notifications channel in Slack
    """
    # os.environ.get() basically conjures up the value referenced by SLACKBOT_TOKEN in the .env file
    # requests.post() takes an optional headers argument that can be passed in as a dictionary like this
    # According to the Slack API documentation for the chat.postMessage endpoint, the token should be passed as an HTTP Authorization header 
    post_headers = {"Authorization": os.environ.get("SLACKBOT_TOKEN")}
    
    # channel is the other required parameter for the chat.postMessage endpoint; was probably redundant to make the channel ID secret but I did anyway 
    # text is the actual string message to be posted in Slack
    post_data = {
        "channel": os.environ.get("TASK_NOTIFICATIONS_CHANNEL_ID"),
        "text": text
    }

    # this is the code that induces the bot to make the post by sending a POST request 
    # The required parameters for this endpoint are the token (post_headers) and channel (post_data)
    # ❓ confused as to why PATCH or POST or PUT all work here as verbs
    requests.post('https://slack.com/api/chat.postMessage', headers=post_headers, data=post_data)


def valid_id_or_400(input_id):
    """
    input: an input id 
    output: a 400 status code if the input ID is not able to be converted to an integer  
    """
    # tries to convert the input_id to an integer
    try:
        return int(input_id)
    # if a ValueError is raised, an abort with 400 gets triggered 
    except ValueError:
        abort(400,{"message": f"ID {input_id} must be an integer", "success": False})


# TASK ENDPOINTS:
#=============================================================================

# this is a decorator that USES the tasks_bp Blueprint to define an endpoint (/<task_id>) and accepted method(s) (GET)  
# This function will execute whenever a request that matches the decorator is received. The name of this function doesn't affect how requests are routed to this method   
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):

    # ❓ Would it make sense to bundle checking for valid task id and querying a task for that id into one instance method or helper function - since I'm doing that for every endpoint
    # This helper function does nothing if task_id is invalid, but aborts with a 400 code if task_id is invalid (instead of raising an error)
    valid_id_or_400(task_id)

    # get_or_404 is a built-in SQLAlchemy Query subclass method that works just like get(), except it aborts with 404 if not found rather than aboridng with None like get() 
    saved_task = Task.query.get_or_404(task_id)

    # convert_to_json is an instance method I created to DRY up repeated code in these 'return response' statements  
    return make_response({"task":(saved_task.convert_to_json())}, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    valid_id_or_400(task_id)

    saved_task = Task.query.get_or_404(task_id)
    
    # Use the request object to get information about the HTTP request; .get_json() specifically gets the JSON body from the request and converts it into a Python dictionary
    form_data = request.get_json()

    saved_task.title = form_data["title"]
    saved_task.description = form_data["description"]
    saved_task.completed_at = form_data["completed_at"]

    # collecting the changes that need to be made - db.session.add() is not needed because nothing new was created
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

    # This conditional statement 
    if toggle_action == "mark_complete":
        # Updates saved_task "completed_at" attribute with current time, in date-time format 
        # using the datetime() class (constructor) of the datetime module
        saved_task.completed_at = datetime.datetime.now()
        db.session.commit()

        # Calling helper function 
        slack_post_to_task_notifications_channel(f"Someone just completed the task {saved_task.title}")

    elif toggle_action == "mark_incomplete":
        saved_task.completed_at = None
        db.session.commit()

    return make_response({"task":(saved_task.convert_to_json())}, 200)


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def task_index():

    # requests.args.get() reads the value attached to the "sort" key from the request route 
    query_sort_direction = request.args.get("sort")
    tasks_response = []

    if query_sort_direction == "asc":
        # asc() and desc() are SQLalchemy module functions (imported above)
        # order_by is another SQLalechemy method that can be used on a Query object 
        # ❓ should probably get some clarity on what both asc() and order_by() are doing to together order the Task query by ascending order and sticking it in a list
        tasks = Task.query.order_by(asc(Task.title))
    elif query_sort_direction == "desc": 
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(task.convert_to_json())

    # ❓ from Flask documentation: jsonify() serializes data to JSON and wraps it in a Response with the application/json mimetype.
    # Used jsonify here instead of makes_response() BECAUSE tasks_response is a list of dictionaries? 
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

    # This is all essentially repurposed code used for Task endpoints above (see above for comments)
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

    # again, request.get_json() gets the JSON body from the HTTP request sent by the client and formats it as a Python dictionary
    # So form_data is a dictionary that will show all the Goal attributes for the goal (with ID goal_id) that we want to assign tasks to 
    form_data = request.get_json()

    # The tasks attribute in this request is a list of whatever tasks the client is requesting to post to this goal
    # Here we're just taking that list out of IDs and sticking it in task_ids
    task_ids = form_data["task_ids"]

    # looping through the list of task ids that the client is requesting to post to this specific goal  
    for each_task_id in task_ids:
        # using each task_id to query a Task object that needs to be updated with its corresponding match_goal_id foreign key
        updated_task = Task.query.get_or_404(each_task_id)
        # grabbing that goal_id from the goal queried above, and assigning that value to the match_goal_id foreign key of each updated task
        # then continuing to loop through until each task in the post request has been updated 
        updated_task.match_goal_id = saved_goal.goal_id

    db.session.commit()

    return make_response({"id": saved_goal.goal_id, "task_ids": task_ids}, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_tasks_for_goal(goal_id):

    valid_id_or_400(goal_id)

    saved_goal = Goal.query.get_or_404(goal_id)
    saved_goal_tasks = []

    # filtering the Task query for tasks with a foreign key id that matches the input goal_id
    tasks = Task.query.filter_by(match_goal_id=goal_id)

    for task in tasks:
        saved_goal_tasks.append(task.convert_to_json())

    response_body = saved_goal.convert_to_json(saved_goal_tasks)

    return make_response(response_body, 200)

    
    

# REFACTORING CONSIDERATIONS:

# Make it so that a task can only be marked completed once (trying to mark a completed task completes returns an error message)









