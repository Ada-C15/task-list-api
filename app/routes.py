from flask import Blueprint, jsonify, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import requests
import os
from app.slackbot import GLaDOS


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def err_404():
    """Helper function for 404 errors"""
    return "", 404


#===============================TASKS===============================#


def retrieve_tasks_ordered_by_title(is_desc=False):
    """Helper function to get all tasks."""

    current_tasks = []

    if is_desc:
        current_tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        current_tasks = Task.query.order_by(Task.title.asc()).all()

    return [task.to_json_format() for task in current_tasks]
        #: 'current_tasks' will store all tasks in the current session.
        #: params: expects a boolean, that will return from the function
        #: below -> is_sort_descending. If is_sort_descending returns
        #: True, it will get the list of current tasks, and order those 
        #: by title in descending order #[::-1]
        #: else, orders titles by ascending order. returns a list of tasks


def is_sort_descending(query_args):
    """Helper function to verify the requested sorting order."""

    if "sort" in query_args and query_args["sort"] == "asc":
        return False

    return True
        #: helper function to check if the query string is asking 
        #: for a specific sorting order (desc to be precise, hence
        #: the name.) a GET request specifies that the sorting should
        #: be *ascending*, returns False and this value will be passed
        #: into 'retrieve_tasks_ordered_by_title' as argument. 
        #: otherwise it returns True, meaning "yes, in descending order"
        #: tried using the bytes returning from request.data, but by 
        #: comparing byte strings I allowed any query 
        #: with matching characters to be passed in the query.
        #: "/?SORTeio_de_trapezio_DESCendente" was ordering by desc. 
        #: if b"sort" in query_str and b"desc" in query_str.. 


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_tasks():
    """Main GET request for tasks"""

    return jsonify(retrieve_tasks_ordered_by_title(is_sort_descending(request.args)))
        #: 1. jsonify() -> jsonifies
        #: 2. retrieve_tasks_ordered_by_title -> gets all tasks (by title)
        #: 3. is_sort_descending -> checks if an order is specifird
        #: 4. request.args -> the arguments in the query, if any


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_task(task_id):
    """Selects a single task with specified ID"""

    single_task = Task.query.get(task_id)

    if not single_task:
        return err_404()

    return jsonify({"task": single_task.to_json_format()})


def validate_field(field, dic):
    """A field validator, accepts a key-value pair (value-key to be precise)"""

    if (field not in dic or dic[field] is None):
        return False
    else:
        return True
            #: checks if a required 'field' is present in a request body,
            #: and if the body is not empty
            #: since we call get_json in the request (data bytes), 
            #: the arguments are like a key-value pair


def post_request_validation(post_request):
    """Helper function to validate post requests' bodies"""

    valid = True
    valid &= validate_field("title", post_request)
    valid &= validate_field("description", post_request)
    valid &= "completed_at" in post_request

    return valid
        #: pythons Bitwise & validation a = a & b
        #: validates a required field and a dictionary (post_request)
        #: using the 'validate_field' helper function in a Bitwise 
        #: validation. Needs to return True for all expressions 
        #: in both sides. We can't call 'validate_field' in "completed_at"
        #: since validate_field would return False if "completed_at" is None.


@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def add_task():
    post_request = request.get_json(request.data)
    validation = post_request_validation(post_request)

    if not validation:
        return {"details": "Invalid data"}, 400

    is_complete_exists = validate_field("is_complete", post_request)

    new_task = Task(title=post_request["title"],
                    description=post_request["description"],
                    completed_at=post_request["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json_format()}), 201


@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    to_update = request.get_json()
    ongoing_task = Task.query.get(task_id)

    if not ongoing_task:
        return err_404()

    ongoing_task.title = to_update["title"]
    ongoing_task.description = to_update["description"]

    db.session.commit()

    return jsonify({"task": ongoing_task.to_json_format()})


@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def discard_task(task_id):
    old_task = Task.query.get(task_id)

    if not old_task:
        return err_404()

    db.session.delete(old_task)
    db.session.commit()

    return jsonify({"details": f'Task {old_task.task_id} "{old_task.title}" successfully deleted'})
        #: Wish I could have used the table name here (maybe there's a way)
        #: return jsonify({"details": f'{old_task.__tablename__}...


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_task_is_complete(task_id):
    ongoing_task = Task.query.get(task_id)

    if not ongoing_task:
        return err_404()

    ongoing_task.completed_at = datetime.utcnow()
    db.session.commit()

    glados = GLaDOS()

    glados.send_request(ongoing_task) # call GLAdOS bot
    return jsonify({"task": ongoing_task.to_json_format()})


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_task_incomplete(task_id):
    ongoing_task = Task.query.get(task_id)

    if not ongoing_task:
        return err_404()

    ongoing_task.completed_at = None
    db.session.commit()

    return jsonify({"task": ongoing_task.to_json_format()})


#===============================GOALS===============================#


@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_goals():
    current_goals = Goal.query.all()
    goals_list = [goal.goal_to_json_format() for goal in current_goals]

    return jsonify(goals_list)


@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def get_goal(goal_id):
    single_goal = Goal.query.get(goal_id)

    if not single_goal:
        return err_404()

    return jsonify({"goal": single_goal.goal_to_json_format()})


@goals_bp.route("", methods=["POST"], strict_slashes=False)
def add_goal():
    goal_request = request.get_json()

    if not validate_field("title", goal_request):
        return {"details": "Invalid data"}, 400

    goal_to_add = Goal(title=goal_request["title"])

    db.session.add(goal_to_add)
    db.session.commit()

    return jsonify({"goal": goal_to_add.goal_to_json_format()}), 201


@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):
    goal_to_update = request.get_json()
    ongoing_goal = Goal.query.get(goal_id)

    if not ongoing_goal:
        return err_404()

    ongoing_goal.title = goal_to_update["title"]
    db.session.commit()

    return jsonify({"goal": ongoing_goal.goal_to_json_format()})


@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def abandon_goal(goal_id):
    ongoing_goal = Goal.query.get(goal_id)

    if not ongoing_goal:
        return err_404()

    db.session.delete(ongoing_goal)
    db.session.commit()

    return jsonify({"details": f'Goal {ongoing_goal.goal_id} "{ongoing_goal.title}" successfully deleted'})


#===========================RELATIONSHIPS===========================#


@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def add_tasks_to_goal(goal_id):
    available_goal = Goal.query.get(goal_id)
    tasks_to_add = request.get_json()

    if not validate_field("task_ids", tasks_to_add):
        return err_404()

    for t in tasks_to_add["task_ids"]:
        task = Task.query.get(t)
        if task is None:
            return err_404()

        task.goal = goal_id
        available_goal.tasks.append(task)
        db.session.add(task)

    db.session.add(available_goal)
    db.session.commit()

    return jsonify(available_goal.add_task_response_to_json())


@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_tasks_for_one_goal(goal_id):
    available_goal = Goal.query.get(goal_id)

    if not available_goal:
        return err_404()

    return jsonify(available_goal.tasks_to_many_goals_to_json_format())


#:TODO: document every function later!!!
#: all tests are passing. yay
#: getting an error that might have something
#: to do with env files.
#: Will investigate this further.