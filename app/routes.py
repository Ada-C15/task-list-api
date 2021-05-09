from app import db
from flask import Blueprint
from .models.task import Task
from .models.goal import Goal
from flask import request
from flask import jsonify, make_response
from sqlalchemy import asc, desc



# creating instance of the class, first arg is name of app's module
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

#create a task with null completed at
@task_bp.route("", methods = ["POST"], strict_slashes = False)
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                description=request_body["description"],
                completed_at = request_body["completed_at"])

        db.session.add(new_task) # "adds model to the db"
        db.session.commit() # does the action above
        return new_task.to_json_response(), 201
    except KeyError:
        return {"details": "Invalid data"}, 400

#Retrieve all /tasks  asc or desc
@task_bp.route("", methods = ["GET"], strict_slashes = False)
def retrieve_tasks_data():
    tasks = Task.query.all() 
    sort_by = request.args.get("sort") # query parameters
    tasks_response = []

    if tasks != None: 
        if sort_by != None and sort_by == "asc": # there are query params (still I need to add that part)
            tasks_asc = Task.query.order_by(Task.title.asc()).all() # this is a list in asc order
            # this puts it in the right order for the response body:
            tasks_response_asc = [task_asc.task_to_json_response() for task_asc in tasks_asc]
            return jsonify(tasks_response_asc), 200
        
        elif sort_by != None and sort_by == "desc":
            tasks_asc = Task.query.order_by(Task.title.desc()).all() # this is a list in asc order
            # this puts it in the right order for the response body:
            tasks_response_desc = [task_asc.task_to_json_response() for task_asc in tasks_asc]
            return jsonify(tasks_response_desc), 200

        for task in tasks:
            tasks_response.append(task.task_to_json_response())
        return jsonify(tasks_response), 200  # returning the list of all tasks
    return jsonify(tasks_response), 200 ## also works as #return tasks_response, 200 ### DOESN'T WORK WITH MAKE RESPONSE!!!!!

# Retrieve one /task/1     
@task_bp.route("/<task_id>", methods=["GET"])
def retrieve_single_task(task_id):
    task = Task.query.get(task_id)
    if task != None:
        return task.to_json_response(), 200

    return make_response('', 404)

#Update a task
@task_bp.route("/<task_id>", methods=["PUT"])  ## DO A TRY EXCEPT WITH DATAERROR
def update_task(task_id):
    task = Task.query.get(task_id)
    if task: # successful updating task
        form_data = request.get_json() # save user input form_data as json format 
        task.title = form_data["title"] # updating model? title field language?
        task.description = form_data["description"] # updating model description field for task = task_id
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return task.to_json_response(), 200
    return make_response(""), 404

# Delete a task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):  # dict_task = task.task_to_json_response()  ==> dict_task["title"]
    task = Task.query.get(task_id) # an object, no format so if I want that, I need to jsonify? {title: "x", "description": "xyz", "completed_at": null}
    if task != None:
        db.session.delete(task)
        db.session.commit()
        details_str = f"Task {task_id} \"{task.title}\" successfully deleted"
    
        return jsonify(details = details_str), 200
        
    return make_response(""), 404

# Modify part of a task to mark complete
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])  ## DO A TRY EXCEPT WITH DATAERROR ??
def patch_task_mark_complete(task_id):
    task = Task.query.get(task_id) ## getting the task by id (it's whole body)
    # PATCHing if: arg mark_complete specified # in URL and task id provided exists in database
    if task:                         
        # then call function that changes it to complete
        task.set_completion() # updates it with a date in "completed_at" field
        print(task.set_completion())
        db.session.commit()
        return task.to_json_response(), 200
    return make_response(""), 404

# Modify part of a task to mark incomplete
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])  ## DO A TRY EXCEPT WITH DATAERROR ??
def patch_task_mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        # task.set_completion() # updates it with a date in "completed_at" field
        task.completed_at = None
        db.session.commit()
        return task.to_json_response(), 200
    return make_response(""), 404

# GOAL ROUTES - works 
@goal_bp.route("", methods = ["POST"], strict_slashes = False)
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal) # "adds model to the db"
        db.session.commit() # does the action above
        return new_goal.goal_to_json_response(), 201
    except KeyError:
        return {"details": "Invalid data"}, 400

#Retrieve all /goals 
@goal_bp.route("", methods = ["GET"], strict_slashes = False)
def retrieve_goals_data():
    goals = Goal.query.all() 
    goals_response = []

    if goals != None:
        for goal in goals:
            goals_response.append(goal.simple_response())
        return jsonify(goals_response), 200  # returning the list of all goals
    return jsonify(goals_response), 200 ## also works as #return goals_response, 200 ### DOESN'T WORK WITH MAKE RESPONSE!!!!!

# Retrieve one /goal/1     
@goal_bp.route("/<goal_id>", methods=["GET"])
def retrieve_single_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal != None:
        return goal.goal_to_json_response(), 200

    return make_response('', 404)

# Delete a goal
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):  
    goal = Goal.query.get(goal_id) # an object, no format so if I want that, I need to jsonify? {title: "x", "description": "xyz", "completed_at": null}
    if goal != None:
        db.session.delete(goal)
        db.session.commit()
        details_str = f"Goal {goal_id} \"{goal.title}\" successfully deleted"
        return jsonify(details = details_str), 200    
    return make_response(""), 404

#Update a goal
@goal_bp.route("/<goal_id>", methods=["PUT"])  ## DO A TRY EXCEPT WITH DATAERROR
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal: # successful updating goal
        form_data = request.get_json() # save user input form_data as json format 
        goal.title = form_data["title"] # updating model? title field language?
        db.session.commit()
        return goal.goal_to_json_response(), 200
    return make_response(""), 404  #NOT FOUND ERROR VS 400 - BAD REQ


# ONE TO MANY RELATIONSHIP - /goals/<goal_id>/tasks
@goal_bp.route("/<goal_id>/tasks", methods = ["POST"])
def post_task_ids_to_goal(goal_id):
    try: 
        request_body = request.get_json()   # should be a dictionary like:
                                            # {"task_ids": [1, 2, 3]}
        goal = Goal.query.get(goal_id)  # the instance of thi goal id including the task ids
        # store list of tasks given in the request body (task_ids)
        task_ids = request_body["task_ids"]  # task_ids - should be a list [1,3,4]
        for task_id in task_ids:
            task = Task.query.get(task_id) # I WANT TASKS WITH THOSE ID S IN TASK IDS 
            # append those tasks that you queried into goal with given id
            goal.tasks.append(task) # this is a field 
            db.session.commit()
        # display this info into response as json 
        return {"id": int(goal_id), "task_ids": task_ids},200
        
    except:
        return make_response(""), 404 ## not found
        # return {"details": "Invalid data"}, 400