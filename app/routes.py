from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def retrieve_tasks_ordered_by_title(is_desc=False):
    """Helper function to get all tasks."""
    current_tasks = []
    if is_desc:
        current_tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        current_tasks = Task.query.order_by(Task.title.asc()).all()
    return [task.to_json_format() for task in current_tasks]
        # 'current_tasks' will store all tasks in the current session.
        # params: expects a boolean, that will return from the function
        # below -> is_sort_descending. If is_sort_descending returns
        # True, it will get the list of current tasks, and order those 
        # by title in descending order #[::-1]
        # else, orders titles by ascending order. returns a list of tasks


def is_sort_descending(query_args):
    if "sort" in query_args and query_args["sort"] == "asc":
        return False
    return True
        # helper function to check if the query string is asking 
        # for a specific sorting order (desc to be precise, hence
        # the name.) a GET request specifies that the sorting should
        # be *ascending*, returns False and this value will be passed
        # into 'retrieve_tasks_ordered_by_title' as argument. 
        # otherwise it returns True, meaning "yes, in descending order"
        # nunca vai ser desc até que se queira o contrário.
        # my first implementation was using the bytes returning from 
        # request.data, but comparing byte strings I allowed any query 
        # with matching characters to be passed in the query!
        # "/?SORTeio_de_trapezio_DESCendente" was ordering by desc. 
        # if b"sort" in query_str and b"desc" in query_str:
        #     return True
        # return False


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_tasks():

    return jsonify(retrieve_tasks_ordered_by_title(is_sort_descending(request.args)))
        # 1. jsonify() -> jsonifies
        # 2. retrieve_tasks_ordered_by_title -> gets all tasks (by title)
        # 3. is_sort_descending -> checks if an order is specifird
        # 4. request.args -> the arguments in the query, if any

@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_task(task_id):
    """Selects a single task with specified ID"""
    single_task = Task.query.get(task_id)
    if single_task is None:
        return "", 404

    return jsonify({"task": single_task.to_json_format()}), 200


def validate_field(field, dic):
    if (field not in dic or dic[field] is None):
        return False
    else:
        return True
            # checks if a required 'field' is present in a request body,
            # and if the body is not empty
            # since we call get_json in the request (data bytes), 
            # the arguments are like a key-value pair


def post_request_validation(post_request):
    valid = True
    valid &= validate_field("title", post_request)
    valid &= validate_field("description", post_request)
    valid &= "completed_at" in post_request
    return valid
        # pythons Bitwise & validation a = a & b
        # validates a required field and a dictionary (post_request)
        # using the 'validate_field' helper function in a Bitwise 
        # validation. Needs to return True for all expressions 
        # in both sides. We can't call 'validate_field' in "completed_at"
        # since validate_field would return False if "completed_at" is None.


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
        return "", 404

    ongoing_task.title = to_update["title"]
    ongoing_task.description = to_update["description"]
    db.session.commit()
    return jsonify({"task": ongoing_task.to_json_format()}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def finish_task(task_id):
    ongoing_task = Task.query.get(task_id)

    if not ongoing_task:
        return "", 404

    db.session.delete(ongoing_task)
    db.session.commit()
    return jsonify({"details": f'Task {ongoing_task.task_id} "{ongoing_task.title}" successfully deleted'})
        # wish I could have used the table name here
        # return jsonify({"details": f'{ongoing_task.__tablename__} {ongoing_task.task_id} "{ongoing_task.title}" successfully deleted'})


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_task_is_complete(task_id):

    ongoing_task = Task.query.get(task_id)
    if not ongoing_task:
        return "", 404

    ongoing_task.completed_at = datetime.utcnow()

    db.session.commit()
    return jsonify({"task": ongoing_task.to_json_format()}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_task_incomplete(task_id):
    ongoing_task = Task.query.get(task_id)
    if not ongoing_task:
        return "", 404

    ongoing_task.completed_at = None

    db.session.commit()
    return jsonify({"task": ongoing_task.to_json_format()}), 200