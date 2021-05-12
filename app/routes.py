from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
import requests
import os

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


####################################################################
#                              GOALS ROUTES                        #
####################################################################

@goals_bp.route("", methods=["GET", "POST"])
def handle_goals():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc": 
            # Automatically sorts by asc
            goals = Goal.query.order_by(goal.title)
        elif sort_query == "desc":
            # SQLAlchemy for sort by desc
            goals = Goal.query.order_by(goal.title.desc())
        else:
            goals = Goal.query.all()
        goals_response = []
        for goal in goals:
            goal_formatted = {
                "id": goal.goal_id,
                "title": goal.title
            }
            goals_response.append(goal_formatted)
        return make_response(jsonify(goals_response), 200)
    elif request.method == "POST":
        request_body = request.get_json()
        # can't use request_body['title'] because of python syntax
        if 'title' in request_body: 
            new_goal = Goal(title=request_body["title"])
            db.session.add(new_goal)
            db.session.commit()
            # uses Goal method to return dictionary
            return make_response(new_goal.goal_data_structure(), 201)
        else:
            return make_response({"details":"Invalid data"}, 400)

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if request.method == "GET":
        return make_response(goal.goal_data_structure(), 200)
    elif request.method == "PUT":
        goal_data = request.get_json()
        goal.title = goal_data["title"]
        db.session.commit()
        return make_response(goal.goal_data_structure(), 200)
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit() 
        goal_response = {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}
        return make_response(goal_response, 200)
    
@goals_bp.route("/<goal_id>/tasks", methods=["GET", "POST"])
def handle_goal_tasks(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if request.method == "GET":
        # Method that appends full task info
        return make_response(goal.tasks_data_structure(), 200)
    if request.method == "POST":
        request_body = request.get_json()
        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal_id
            db.session.commit()
        return make_response({"id": goal.goal_id, "task_ids": request_body["task_ids"]}, 200)


####################################################################
#                              TASK ROUTES                        #
####################################################################

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc": 
            tasks = Task.query.order_by(Task.title)
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.all()
            
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.task_data_structure()['task'])

        return make_response(jsonify(tasks_response), 200)

    elif request.method == "POST":
        request_body = request.get_json()
        if 'title' in request_body and 'description' in request_body and 'completed_at' in request_body: 
            new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body['completed_at'])
            db.session.add(new_task)
            db.session.commit()
            return make_response(new_task.task_data_structure(), 201)
        else:
            return make_response({"details":"Invalid data"}, 400)


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == "GET":
        return make_response(task.task_data_structure(), 200)
    elif request.method == "PUT":
        task_data = request.get_json()
        task.title = task_data["title"]
        task.description = task_data["description"]
        task.completed_at = task_data['completed_at']
        db.session.commit()
        task = Task.query.get(task_id)
        return make_response(task.task_data_structure(), 200)

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit() 
        task_response = {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}
        return make_response(jsonify(task_response), 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def handle_complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.update_completed() # function in Task Module to Update Time
    db.session.commit() 
    # uses Slack API to interact with a slackbot + post to channel
    url = f"https://slack.com/api/chat.postMessage?channel=general&text={'Hello Testing'}"
    auth_token = os.environ.get("API_KEY")
    headers = {'Authorization': auth_token}
    # No Payload as text is sent via query string
    response = requests.request("POST", url, headers=headers)
    return make_response(task.task_data_structure(), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def handle_incomplete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed_at = None
    db.session.commit() 
    return make_response(task.task_data_structure(), 200)