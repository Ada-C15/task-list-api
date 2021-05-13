from app import db
from flask import request, Blueprint, jsonify
from .models.task import Task
from .models.goal import Goal
import datetime
import requests
import os


### WAVES 1 AND 2 - CRUD for TASKS

# Create an endpoint specifically for tasks (all the routes start with /tasks):
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False


# define a route with default empty string to GET all tasks:
@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by("title")
    elif sort_query == "desc":
        tasks = Task.query.order_by("title desc")        # using string allows us to be more specific in our queries
        tasks = Task.query.order_by(Task.title.desc())  # same as above
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        # tasks_response.append(task.to_json()) # same as below
        if task.completed_at == None:
            tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
        else:
            tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
            })

    return jsonify(tasks_response), 200


# define a route with default empty string for POST:
@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():  

    request_body = request.get_json()

    # if not request_body["title"] or not request_body["description"]:  # triggers key error
    if not request_body.get("title") or not request_body.get("description"):
        return jsonify({"details": "Invalid data"}), 400 

    try:
        request_body["completed_at"] == None
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400 

    new_task = Task(title = request_body["title"], \
        description = request_body["description"], \
        completed_at = request_body["completed_at"])

    db.session.add(new_task)   
    db.session.commit()  

    # we need an extra step to transfer completed_at to is_completed:
    task_dict = new_task.to_dict()

    return jsonify({"task": task_dict}), 201


# define a new route to GET a specific task
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_one_task(task_id):

    if not is_int(task_id):        
        return {"message": f"ID {task_id} must be an integer"}, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404
    else:
        task_dict = task.to_dict()
     
    return jsonify({"task": task_dict}), 200


# define a new route to update (PUT) one task by its id (route parameter between <>, treated as a variable):
@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_single_task(task_id):

    if not is_int(task_id):        
        return {"message": f"ID {task_id} must be an integer"}, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    form_data=request.get_json()
    task.title=form_data["title"]
    task.description=form_data["description"]
    task.completed_at=form_data["completed_at"]
    db.session.commit()

    # we need an extra step to transfer completed_at to is_completed:
    task_dict = task.to_dict()
    
    return jsonify({"task": task_dict}), 200


# define a new route to DELETE one task by its id (route parameter between <>, treated as a variable):
@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_task(task_id):

    if not is_int(task_id):        
        return {"message": f"ID {task_id} must be an integer"}, 400

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404
   
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200


### WAVE 3 - PATCH ROUTES for TASKS

# define a new route to update (PATCH) one task by its id (route parameter between <>, treated as a variable):
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):

    if not is_int(task_id):        
        return {"message": f"ID {task_id} must be an integer"}, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    # if task.completed_at != None:
    #     return 

    task.completed_at=datetime.datetime.now()
    post_message(task.title)
    db.session.commit()

    # we need an extra step to transfer completed_at to is_completed:
    task_dict = task.to_dict()
    
    return jsonify({"task": task_dict}), 200

def post_message(task_title):
    requests.post("https://slack.com/api/chat.postMessage", \
            headers={"Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"}, \
                data={"channel": f"{os.environ.get('SLACK_CHANNEL')}", "text":f"Someone just completed the task {task_title}"})



# define a new route to update (PATCH) one task by its id (route parameter between <>, treated as a variable):
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):

    # check whether task_id is an int:
    if not is_int(task_id):        
        return {"message": f"ID {task_id} must be an integer"}, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    if task.completed_at != None:
        task.completed_at = None
        task.is_complete = False

    db.session.commit()
                                                                                                                                                                    
    task_dict = task.to_dict()
        
    return jsonify({"task": task_dict}), 200



### WAVE 5 - CRUD for GOALS

# Create an endpoint specifically for goals (all the routes start with /goals):
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# define a route with default empty string to GET all goals:
@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_goals():

    goals = Goal.query.all() 
    # build list that has all the goals in it:
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())   

    return jsonify(goals_response), 200


# define a route with default empty string for POST:
@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():  

    request_body = request.get_json()

    # if not request_body["title"]:  # triggers key error
    if not request_body.get("title"):
        return jsonify({"details": "Invalid data"}), 400 
 
    new_goal = Goal(title = request_body["title"])

    db.session.add(new_goal)   
    db.session.commit()  

    # we need an extra step to transfer json to dict:
    goal_dict = new_goal.to_dict()

    return jsonify({"goal": goal_dict}), 201


# define a new route to GET a specific goal
@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def get_one_goal(goal_id):

    if not is_int(goal_id):        
        return {"message": f"ID {goal_id} must be an integer"}, 400
    
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404
    else:
        goal_dict = goal.to_dict()
     
    return jsonify({"goal": goal_dict}), 200


# define a new route to update (PUT) one goal by its id (route parameter between <>, treated as a variable):
@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_single_goal(goal_id):

    if not is_int(goal_id):        
        return {"message": f"ID {goal_id} must be an integer"}, 400
    
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    form_data=request.get_json()
    goal.title=form_data["title"]

    db.session.commit()

    # we need an extra step to transfer json to dict:
    goal_dict = goal.to_dict()
    
    return jsonify({"goal": goal_dict}), 200


# define a new route to DELETE one goal by its id (route parameter between <>, treated as a variable):
@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_goal(goal_id):

    if not is_int(goal_id):        
        return {"message": f"ID {goal_id} must be an integer"}, 400

    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404
   
    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200


### WAVE 6 - ONE TO MANY RELATIONSHIP BETWEEN TASKS AND GOALS

# All of our tasks are going to be nested inside of each GOAL, all routes will start with :
# /goals/<goal_id>/tasks

# GET all the tasks within a specific goal/no matching tasks?/no matching goal?
@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_single_goal_tasks(goal_id):

    if not is_int(goal_id):        
        return {"message": f"ID {goal_id} must be an integer"}, 400

    goal = Goal.query.get(goal_id)
    if goal is None:
        return jsonify(None), 404

    goal_tasks = Task.query.filter(Task.goals_id==goal.id)

    goal_tasks_response = []
    for task in goal_tasks:
        goal_tasks_response.append(task.to_dict())
    
    goal_tasks_dict = {
        "id": goal.id,
        "title": goal.title,
        "tasks": goal_tasks_response
    }

    # goal_tasks_dict = goal_tasks_response.to_dict()

    return jsonify(goal_tasks_dict), 200


# POST all the tasks within a specific goal
@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def add_task_ids_to_goal(goal_id):
    request_body = request.get_json()
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goals_id = goal.id
    
    # db.session.add(???)   
    db.session.commit()  
    
    return jsonify({
            "id": goal.id,
            "task_ids": request_body["task_ids"]
        }), 200


# Send a list of task id's to a goal (task_ids)


# Delete a task within a specific goal???

