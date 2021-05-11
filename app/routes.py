from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime
from app.slack import slack_message
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


# -------------- CRUD for Tasks ---------------------------


@tasks_bp.route("", methods=["GET"])
def handle_tasks_get():
    """
    - Get all saved tasks.
    - Get all saved tasks filtered by title in asc and desc order.
    """

    if not request.args:
        tasks = Task.query.all()
    else:
        sort_query = request.args.get("sort", default=None, type=str)

        if sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        elif sort_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        else:
            return jsonify(
                "Parameter sort is not defined. Use ?sort=desc or ?sort=asc to sort the tasks by title."), 404

    tasks_response = [task.to_json() for task in tasks]

    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_one_task_get(task_id):
    """
    Get specific tasks by id.
    """
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    response_body = {"task": task.to_json()}
    return (response_body, 200)


@tasks_bp.route("", methods=["POST"])
def handle_tasks_post():
    """
    Create a Task.
    """
    request_body = request.get_json()

    if ("title" not in request_body.keys()) or (
        "description" not in request_body.keys()) \
            or ("completed_at" not in request_body.keys()):
        return make_response({
            "details": "Invalid data"
        }, 400)

    new_task = Task()
    new_task = new_task.from_json(request_body)

    db.session.add(new_task)
    db.session.commit()

    # todo: retrieve committed task to the db, not the one with id 1
    retrieve_task = Task.query.get(new_task.task_id)

    return {"task": retrieve_task.to_json()}, 201


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def handle_one_task_delete(task_id):
    """
    Delete task with specific id.
    """
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    db.session.delete(task)
    db.session.commit()
    return (
        {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def handle_one_task_update(task_id):
    """
    Update task with specific id.
    """
    task = Task.query.get(task_id)

    if task is None:  # task not found
        return jsonify(None), 404

    data_to_update_with = request.get_json()
    task = task.from_json(data_to_update_with)

    db.session.commit()

    retrieve_task = Task.query.get(task.task_id)

    return ({"task": retrieve_task.to_json()}, 200)


def slack_send_message():
    path = "https://slack.com/api/chat.postMessage"
    auth = f'Bearer {os.environ.get("SLACK_BOT_TOKEN")}'

    print(auth)

    query_params = {
        "channel": "task-notifications",
        "text": f"Hello! Current date: {datetime.now()}"
    }

    headers = {
        "Authorization": auth
    }

    slask_request = requests.post(path,
                                  params=query_params,
                                  headers=headers)
    print(slask_request)
    # print(slask_request.json())
    return slask_request


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def handle_one_task_complete_patch(task_id):
    """
    Mark Complete on an Incompleted Task
    """
    # if True:
    #     slack_message()

    task = Task.query.get(task_id)

    if task is None:  # task not found
        return jsonify(None), 404

    task.completed_at = datetime.utcnow()
    db.session.commit()

    retrieve_task = Task.query.get(task.task_id)

    message = f"Someone just completed the task '{retrieve_task.title}'."
    slack_message(message)

    return ({"task": retrieve_task.to_json()}, 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def handle_one_task_incomplete_patch(task_id):
    """
    Mark InComplete on an Completed Task
    """
    task = Task.query.get(task_id)

    if task is None:  # task not found
        return jsonify(None), 404

    task.completed_at = None
    db.session.commit()
    retrieve_task = Task.query.get(task.task_id)
    return ({"task": retrieve_task.to_json()}, 200)


# -------------- CRUD for Goals ---------------------------


@goals_bp.route("", methods=["POST"])
def handle_goal_post():
    """
    - Create new goal.
    """

    request_body = request.get_json()

    if "title" not in request_body.keys():
        return make_response({"details": "Invalid data"}, 400)

    new_goal = Goal(title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    retrieve_goal = Goal.query.get(new_goal.goal_id)

    return make_response({"goal": retrieve_goal.to_json()}, 201)


@goals_bp.route("", methods=["GET"])
def handle_goals_get():
    """
    - Get all saved goals.
    """
    goals = Goal.query.all()
    goals_response = [goal.to_json() for goal in goals]
    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_one_goal_get(goal_id):
    """
    Get specific goal by id.
    """

    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    return ({"goal": goal.to_json()}, 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def handle_one_goal_delete(goal_id):
    """
    Delete goal with specific id.
    """

    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    db.session.delete(goal)
    db.session.commit()

    return ({"details": f'Goal {goal_id} \"{goal.title}\" successfully deleted'}, 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def handle_one_goal_update(goal_id):
    """
    Update goal with specific id.
    """

    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    data_to_update_with = request.get_json()
    goal.title = data_to_update_with["title"]

    db.session.commit()

    retrieve_goal = Goal.query.get(goal.goal_id)

    return ({"goal": retrieve_goal.to_json()}, 200)


# ----- Establishing one-to-many relationship between goals and tasks --------
# /goals/<goal_id>/tasks

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def handle_one_goal_many_tasks_get(goal_id):
    """
    Sending a List of Task IDs to a Goal with specific ID.
    """

    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    request_body = request.get_json()
    tasks_ids_to_belong = request_body["task_ids"]

    for task_id in tasks_ids_to_belong:
        task = Task.query.get(task_id)
        task.goal_id = int(goal_id)
        db.session.commit()

    response_body = goal.to_json()

    return (response_body, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def handle_tasks_of_goal_get(goal_id):
    """
    Getting Tasks of One Goal
    """
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    tasks = goal.tasks
    tasks_list = [task.to_json() for task in tasks]

    response_body = {
        "id": int(goal_id),
        "title": goal.title,
        "tasks": tasks_list
    }

    return (response_body, 200)
