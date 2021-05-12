from flask import Blueprint, request, make_response
from flask import jsonify
from app import db, slack_key, slack_channel
from app.models.task import Task
from app.models.goal import Goal
import datetime
import requests

# class Task routes
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def handle_tasks():

    if request.method == "POST":

        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return jsonify({
                "details": "Invalid data"
            }), 400
        
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()

        return new_task.to_json(), 201

    if request.method == "GET":

        sort_query = request.args.get("sort")
        title_query = request.args.get("title")

        if sort_query == 'asc':
            tasks = Task.query.order_by(Task.title)
        elif sort_query == 'desc':
            tasks = Task.query.order_by(Task.title.desc())
        elif sort_query == 'id':
            tasks = Task.query.order_by(Task.task_id)
        elif title_query:
            tasks = Task.query.filter_by(title=title_query)
        else: 
            tasks = Task.query.all()
        
        task_list = []

        for task in tasks: 
            task_list.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.check_if_complete()
            })
            
        return jsonify(task_list)


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return "", 404

    if request.method == "GET":
        return task.to_json()
    
    if request.method == "PUT":

        task_data = request.get_json()

        task.title = task_data["title"]
        task.description = task_data["description"]
        task.completed_at = task_data["completed_at"]

        db.session.commit()

        return task.to_json()

    if request.method == "DELETE":

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "details": f'Task {task.task_id} "{task.title}" successfully deleted'
        }) 


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_task_complete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return "", 404 

    if request.method == "PATCH":
        
        task.completed_at = datetime.datetime.now()
        db.session.commit()

        query_params = {
        "channel": slack_channel,
        "text": f"Someone just completed the task {task.title}"
        }

        header_data = {
            "authorization": slack_key
        }

    response = requests.post('https://slack.com/api/chat.postMessage', headers=header_data, params=query_params)

    return task.to_json()


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_task_incomplete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return "", 404 

    if request.method == "PATCH":
        
        task.completed_at = None
        db.session.commit()

        return task.to_json()


# class Goal routes
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST", "GET"])
def handle_goals():

    if request.method == "POST":

        request_body = request.get_json()

        if not request_body:
            return jsonify({
                "details": "Invalid data"
            }), 400
        
        new_goal = Goal(title=request_body["title"])
        
        db.session.add(new_goal)
        db.session.commit()

        return new_goal.to_json(), 201

    if request.method == "GET":

        title_query = request.args.get("title")

        if title_query:
            goals = Goal.query.filter_by(title=title_query)
        else:
            goals = Goal.query.all()

        goal_list=[]

        for goal in goals: 
            goal_list.append({
                "id": goal.goal_id,
                "title": goal.title,
            })
            
        return jsonify(goal_list)


@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        return "", 404

    if request.method == "GET":
        return goal.to_json()
    
    if request.method == "PUT":

        goal_data = request.get_json()
        
        goal.title = goal_data["title"]
        db.session.commit()

        return goal.to_json()

    if request.method == "DELETE":

        db.session.delete(goal)
        db.session.commit()

        return jsonify({
            "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
        }) 


@goals_bp.route("<goal_id>/tasks", methods=["POST", "GET"], strict_slashes=False)
def handle_goal_tasks(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        return "", 404

    if request.method == "POST":

        request_body = request.get_json()

        associated_tasks = []

        for task_id in request_body["task_ids"]:

            task = Task.query.get(task_id)
            task.goal_id = goal_id

            db.session.commit()

            associated_tasks.append(task.task_id)
        
        return {
            "id": goal.goal_id,
            "task_ids": associated_tasks
        }
    
    if request.method == "GET":
        
        associated_tasks = Task.query.filter_by(goal_id=goal_id)

        list_of_tasks = []

        for task in associated_tasks:
            list_of_tasks.append({
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.check_if_complete()
            })

        return {
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": list_of_tasks
            }