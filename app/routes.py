from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
import datetime
import os
import requests
from dotenv import load_dotenv
load_dotenv()

'''
Wave 01 and 02: Get All Tasks (can sort through these tasks by title) and Post A Task
'''
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])

def handle_tasks():
    if request.method == "GET":
        query_param_value = request.args.get("sort")
        if query_param_value == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif query_param_value == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            tasks_response.append(task.to_dict())
            # tasks_response.append({
            #     "id": task.id,
            #     "title": task.title,
            #     "description": task.description,
            #     "is_complete": task.is_complete
            # })
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        
        # Invalid task if missing title, description, or completed_at     
        if "completed_at" not in request_body or "description" not in request_body or "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
            # return jsonify(details="Invalid data"), 400           
        else:
            new_task = Task(
                title = request_body["title"],
                description = request_body["description"],
                completed_at = request_body["completed_at"])
        
            # add this model to the database and commit the changes
            db.session.add(new_task)
            db.session.commit()

            # return jsonify(task= {
            # "id": new_task.id,
            # "title": new_task.title,
            # "description": new_task.description,
            # "is_complete": True if new_task.completed_at is not None else False
            # }), 201
            return make_response({"task" : new_task.to_dict()}, 201)


'''
Get One Task, Update One Task, Delete One Task
'''
@tasks_bp.route("/<task_id>", methods=["GET","PUT","DELETE"], strict_slashes=False)
def handle_single_task(task_id):

    # Find the task with the given id
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
        # return make_response(jsonify(None), 404)

    if request.method == "GET": 
        # return make_response(jsonify(task= {
        # "id": task.id,
        # "title": task.title,
        # "description": task.description,
        # "is_complete": True if task.completed_at is not None else False
        # }), 200)
        return {"task" : task.to_dict()}
    
    elif request.method == "PUT":
        new_data = request.get_json()

        task.title = new_data["title"]
        task.description = new_data["description"]
        task.completed_at = new_data["completed_at"]

        db.session.commit()

        return make_response({"task" : task.to_dict()}, 200)

        # return jsonify(task= {
        #     "id": task.id,
        #     "title": task.title,
        #     "description": task.description,
        #     "is_complete": True if task.completed_at is not None else False
        # }), 200

        # return make_response(jsonify(task=task.to_dict()), 200)
        
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()

        return make_response({"details": f"Task {task.id} \"{task.title}\" successfully deleted"}, 200)
        # return make_response(jsonify(details=f"Task {task.id} \"{task.title}\" successfully deleted"), 200)

'''
Wave 03: Mark a task complete or incomplete
'''
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    if request.method == "PATCH":

        task.completed_at = datetime.datetime.now()

        db.session.commit()

        send_slack(task)

        return {"task" : task.to_dict()}

        # return jsonify(task= {
        #     "id": task.id,
        #     "title": task.title,
        #     "description": task.description,
        #     "is_complete": bool(task.completed_at)
        # }), 200
    
    return("PATCH method only. Do not accept other methods for this route.")

'''
Wave 04: Notify user a task was completed with Slack messages, using the Slack web API.
'''
def send_slack(task):

        text = f"Someone just completed the task {task.title}"
        path = f"https://slack.com/api/chat.postMessage?channel=task-notifications&text={text}"
        token = os.environ.get("API_KEY")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.request("POST", path, headers=headers)
        
        return response


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    if request.method == "PATCH":

        task.completed_at = None

        db.session.commit()

        return {"task" : task.to_dict()}

        # return jsonify(task= {
        #     "id": task.id,
        #     "title": task.title,
        #     "description": task.description,
        #     "is_complete": bool(task.completed_at)
        # }), 200

    return("PATCH method only. Do not accept other methods for this route.")
    
'''
Wave 05: CRUD for Goal
'''
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET", "POST"])

def handle_goals():
    if request.method == "GET":
        query_param_value = request.args.get("sort")
        if query_param_value == "asc":
            goals = Task.query.order_by(Goal.title.asc())
        elif query_param_value == "desc":
            goals = Task.query.order_by(Goal.title.desc())
        else:
            goals= Goal.query.all()

        goals_response = []
        for goal in goals:
            goals_response.append(goal.to_dict())
        return jsonify(goals_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        
        # Invalid goal if missing title
        if "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        else:
            new_goal = Goal(
                title = request_body["title"])
        
            db.session.add(new_goal)
            db.session.commit()

            return make_response({"goal" : new_goal.to_dict()}, 201)

@goals_bp.route("/<goal_id>", methods=["GET","PUT","DELETE"], strict_slashes=False)
def handle_single_goal(goal_id):

    # Find the goal with the given id
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    if request.method == "GET": 
        return make_response({"goal" : goal.to_dict()})

    elif request.method == "PUT":
        new_data = request.get_json()

        goal.title = new_data["title"]

        db.session.commit()

        return make_response(jsonify(goal=goal.to_dict()), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(goal)
        db.session.commit()

        return make_response({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}, 200)

'''
Wave 06: Goal with tasks. POST tasks to a goal. GET tasks under a goal.
'''
@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def post_tasks_to_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    # json body in Postman, what to be posted
    request_data = request.get_json() 
        
    for task_no in request_data["task_ids"]: # see line 26-27 in test. For task_no in task_ids": [1, 4], loop through task_no ([1,4])
        task = Task.query.get(task_no) # find the task in the Task model that has that id
        task.goal_id = goal.id # this line creates relationship in db. Assign goal.id from the Goal model to the foreign key in the Task model to the task belongs to that goal. Now that goal has that task. 

    db.session.commit()

    return {
        "id" : goal.id, 
        "task_ids" : request_data["task_ids"]
    }

@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_tasks(goal_id):

    # find the goal with the specific goal id
    goal = Goal.query.get(goal_id)
    
    if goal is None:
        return make_response("", 404)
    
    tasks = Task.query.filter_by(goal_id=goal.id)

    # For query-params, if route is /goal/tasks/?=goal_id
    # goal_query = request.args.get("goal_id")
    # tasks = Task.query.filter_by(goal_id=goal_query)

    list_of_tasks = []
    for task in tasks: 
        list_of_tasks.append(task.to_dict())
    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": list_of_tasks
    }
