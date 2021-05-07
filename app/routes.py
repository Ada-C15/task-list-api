from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def retrieve_tasks_ordered_by_title(is_desc=False):
    current_tasks = []
    if is_desc:
        current_tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        current_tasks = Task.query.order_by(Task.title.asc()).all()
    return [task.to_json_format() for task in current_tasks]
        # old!
        # def retrieve_by_title(is_desc=False):
        # current_tasks = Task.query.order_by(Task.title).all()
        # task_list = [task.to_json_format() for task in current_tasks]
        # if is_desc:
        #     return task_list[::-1]
        # return task_list  


def is_sort_descending(query_args):
    if "sort" in query_args and query_args["sort"] == "asc":
        return False
    return True
        # old! just to keep track of what I have tried and changed:
        # if b"sort" in query_str and b"desc" in query_str:
        #     return True
        # return False
        # unfortunately, "/?SORTeio_de_trapezio_DESCendente" will 
        # be sorted by desc so I my bytes are uselesssss

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_tasks():

    return jsonify(retrieve_tasks_ordered_by_title(is_sort_descending(request.args)))
        # byte_string = request.query_string :(
        # if is_sort_descending(byte_string):
        #     all_tasks = retrieve_by_title(True)
        # else:
        #     all_tasks = retrieve_by_title()

@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_task(task_id):

    single_task = Task.query.get(task_id)
    if single_task is None:
        return "", 404

    return jsonify({"task": single_task.to_json_format()}), 200


def validate_field(field, dic):
    if (field not in dic or dic[field] is None):
        return False
    else:
        return True

# v &= v -> v = v && v THIS WORKS :p

def post_request_validation(post_request):
    # pythons Bitwise & validation a = a & b
    valid = True
    valid &= validate_field("title", post_request)
    valid &= validate_field("description", post_request)
    valid &= "completed_at" in post_request
    return valid


@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def add_task():
    post_request = request.get_json(request.data)
    # print(post_request)
    # print("*********")
    validation = post_request_validation(post_request)
    if not validation:
        return {"details": "Invalid data"}, 400

    is_complete_exists = validate_field("is_complete", post_request)
    complete = post_request["is_complete"] if is_complete_exists else False

    new_task = Task(title=post_request["title"],
                    description=post_request["description"],
                    completed_at=post_request["completed_at"],
                    is_complete=complete)
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
    # ongoing.completed_at = to_update["completed_at"]
    db.session.commit()
    return jsonify({"task": ongoing_task.to_json_format()}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def finish_task(task_id):
    to_drop = request.get_json()
    ongoing_task = Task.query.get(task_id)

    if not ongoing_task:
        return "", 404

    db.session.delete(ongoing_task)
    db.session.commit()
    return jsonify({"details": f'Task {ongoing_task.task_id} "{ongoing_task.title}" successfully deleted'})
        # wish I could have used the table name here
        # return jsonify({"details": f'{ongoing_task.__tablename__} {ongoing_task.task_id} "{ongoing_task.title}" successfully deleted'})
