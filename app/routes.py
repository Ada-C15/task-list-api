from app import db 
from .models.task import Task
from .models.goal import Goal
from flask import request, Blueprint, make_response, Response, jsonify
from sqlalchemy import desc
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

####################### POST TASK CRUD - CREATE #############################
@tasks_bp.route("", methods=["POST"]) # The route usually starts with the model plural - but the tasks_bp Blueprint - is already providing the url_prefix="/tasks"
def create_task(): # this function will execute when a request matched the decoractor. 
    request_body = request.get_json() # the local variable request_body will hold the body contents of the HTTP request in a Python data structre (likely dictionaries, lists, and strings)
    # request.get_json() ^^ use the request object <<imported from flask>> to get information about the HTTP request - the method .get_json() grabs the part of the HTTP request_body that's in JSON format
    
    ### if request_body['title'] == None: # there is no key in the request_body called title because the client didnt input correctly
###############
    if 'title' not in request_body.keys(): # this condition works withour the keys() function too
        response_bod = {"details": "Invalid data"}
        return jsonify(response_bod), 400
    elif 'description' not in request_body.keys():
        response_bod = {"details": "Invalid data"}
        return jsonify(response_bod), 400
    elif 'completed_at' not in request_body.keys():
        response_bod = {"details": "Invalid data"}
        return jsonify(response_bod), 400
###############
    else:
        new_task = Task(title=request_body["title"], # We can create an instance of Task using the data in request_body. We assign this new instance to the new_task variable
                    description=request_body["description"], #use keyword arguments that match our model attribute, and access the request_body values to create the Task instance
                    completed_at=request_body["completed_at"])
        db.session.add(new_task) # adds the task model to the database
        db.session.commit() # saves the task to the database
        jsonable_new_task = new_task.to_dictionary()
    # for each endpoint - we must return the HTTP response

        return jsonify(task=jsonable_new_task), 201

# make_response() function instantiates a Response object. A Response object is generally what we want to return from Flask endpoint functions.

####################### GET ALL TASKS - CRUD - READ #######################################
############# GET ALL TASKS - ASCENDING or DESCENDING - CRUD - READ #######################
@tasks_bp.route("", methods=["GET"]) 
def get_all_tasks():
    tasks = Task.query.all()
    sort_by_title = request.args.get("sort")
    
    if sort_by_title == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_by_title == "desc":
        tasks = Task.query.order_by(desc(Task.title))

    tasks_response = []
    for t in tasks: 
        each_task = t.to_dictionary()
        tasks_response.append(each_task)
    return jsonify(tasks_response), 200

# tasks_response contains a list of book dictionaries. 
# -- To turn it into a Response object, we pass it into jsonify(). This will be my practice when --
# -- returning a list of something because the make_response function does not handle lists.

####################### GET ONE TASK by ID - CRUD - READ #############################
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if task:
        response = {
            "id": task.id,
            "title": task.title,
            "description": task.description
        }
        return jsonify(task=task.to_dictionary()), 200
    else:
        response = None
        return jsonify(response), 404

####################### PUT TASK CRUD - UPDATE #############################
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    update_task = Task.query.get(task_id)
    if update_task is None:
        return jsonify(None), 404
    else:
        request_in_json = request.get_json()

        update_task.title = request_in_json["title"]
        update_task.description = request_in_json["description"]
        update_task.completed_at = request_in_json["completed_at"]

        # Save Action
        db.session.commit()
    
        jsonable_update_task = update_task.to_dictionary()

        return jsonify(task=jsonable_update_task), 200

####################### DELETE TASK - CRUD - DELETE #############################
@tasks_bp.route("/<task_id>", methods=["DELETE"]) 
def delete_tasks(task_id):
    delete_task = Task.query.get(task_id)
    if delete_task is None:
        return jsonify(None), 404
    else:
    
        db.session.delete(delete_task) # deletes the model from the database
        db.session.commit() # Save Action
    
        response_body = f"Task {task_id} \"{delete_task.title}\" successfully deleted"

        return jsonify(details=response_body), 200

####################### PATCH MARK COMPLETED_AT - CRUD - UPDATE #############################
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"]) 
def mark_complete(task_id):
    task_to_update = Task.query.get(task_id)
    if task_to_update is None:
        return jsonify(None), 404
    else:
        request_in_json = request.get_json()
        task_to_update.completed_at = datetime.now()

        db.session.commit()
            
        jsonable_status_updated = task_to_update.to_dictionary()

        return jsonify(task=jsonable_status_updated), 200

####################### PATCH MARK INCOMPLETED - CRUD - UPDATE #############################
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"]) 
def mark_incomplete(task_id):
    task_to_update = Task.query.get(task_id)
    if task_to_update is None:
        return jsonify(None), 404
    else:
        request_in_json = request.get_json()
        task_to_update.completed_at = None

        db.session.commit()
            
        jsonable_status_updated = task_to_update.to_dictionary()

        return jsonify(task=jsonable_status_updated), 200


####################### POST GOAL CRUD - CREATE #############################
@goals_bp.route("", methods=["POST"]) 
def create_goal(): 
    request_body = request.get_json()
###############
    if 'title' not in request_body.keys(): # this condition works withour the keys() function too
        response_bod = {"details": "Invalid data"}
        return jsonify(response_bod), 400
###############
    else:
        new_goal = Goal(title=request_body["title"])

        db.session.add(new_goal) # adds the goal model to the database
        db.session.commit() # saves the goal to the database
        
        jsonable_new_goal = new_goal.to_dictionary()

        return jsonify(goal=jsonable_new_goal), 201

####################### DELETE GOAL - CRUD - DELETE #############################
######### MUST HAVE A GET GOAL WORKING BEFORE DELETE CAN WORK ########
@goals_bp.route("/<goal_id>", methods=["DELETE"]) 
def delete_goal(goal_id):
    delete_goal = Goal.query.get(goal_id)
    if delete_goal is None:
        return jsonify(None), 404
    else:
        db.session.delete(delete_goal) # deletes the model from the database
        db.session.commit() # Save Action
    
        response_body = f"Goal {goal_id} \"{delete_goal.title}\" successfully deleted"

        return jsonify(details=response_body), 200


####################### GET ALL GOALS - CRUD - READ #######################################
@goals_bp.route("", methods=["GET"]) 
def get_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for g in goals: 
        each_goal = g.to_dictionary()
        goals_response.append(each_goal)
    return jsonify(goals_response), 200

####################### GET ONE GOAL by ID - CRUD - READ #############################
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        response = {
            "id": goal.id,
            "title": goal.title
        }
        return jsonify(goal=goal.to_dictionary()), 200
    else:
        response = None
        return jsonify(response), 404

####################### PUT GOAL CRUD - UPDATE #############################
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    update_goal = Goal.query.get(goal_id)
    if update_goal is None:
        return jsonify(None), 404
    else:
        request_in_json = request.get_json()

        update_goal.title = request_in_json["title"]

        # Save Action
        db.session.commit()
    
        jsonable_update_goal = update_goal.to_dictionary()

        return jsonify(goal=jsonable_update_goal), 200


###################### RELATIONAL REQUESTS ###########################

####################### POST TASK_IDs to GOAL CRUD - CREATE #############################
@goals_bp.route("/<goal_id>/tasks", methods=["POST"]) 
def post_task_ids_to_goal(goal_id): 
    # goal_to_update = Goal.query.get(goal_id)
    request_in_json = request.get_json()

    new_task_ids = request_in_json["task_ids"]
    for t in new_task_ids:
        task_to_update = Task.query.get(t)
        # goal_to_update.tasks.append(task_to_update) -- what?
        task_to_update.goal_id = goal_id
    db.session.commit() # saves the goal to the database
        
    response_body = {
        "id": int(goal_id),
        "task_ids": new_task_ids
    }

    return jsonify(response_body), 200

        ###########
    # if 'title' not in request_body.keys(): # this condition works withour the keys() function too
    #     response_bod = {"details": "Invalid data"}
    #     return jsonify(response_bod), 400
        ###########

####################### GET TASK for GOAL CRUD - READ #############################
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal:
        tasks_in_dictionary = []
        for t in goal.tasks:
            tasks_in_dictionary.append(t.to_dictionary())
        
        response = {
            "id": goal.id,
            "title": goal.title,
            "tasks": tasks_in_dictionary
        }
    
        return jsonify(response), 200
    else:
        response = None
        return jsonify(response), 404