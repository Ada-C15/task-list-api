from app import db
from .models.task import Task
from .models.goal import Goal
from flask import request, Blueprint, make_response, jsonify, Response
from sqlalchemy import desc, asc
from datetime import date

#WAVE 1 CRUD
task_list_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

#WAVE 1 CREATE NEW TASK
@task_list_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    
    #CREATE A TASK WITH MISSING DATA
    if ("title" not in request_body or 
        "description" not in request_body or 
        "completed_at" not in request_body):
        
        return jsonify(details="Invalid data"),400
    
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()
    
    return new_task.to_json(), 201
    
    #if task_completed == False:
    #     return make_response("task_id": self.task_id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": False 
    #     }), 201
    # else:    
    #     return make_response(jsonify(new_task, 201)
    
    #Optional enhancement : when creating a task, the value of completed_at is a string that is not a datetime?                        

@task_list_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    
    sort_by_title_order = request.args.get("sort")
    
    tasks_list = []
    
    if sort_by_title_order is not None:
        if (sort_by_title_order == "asc"):
            tasks_list = db.session.query(Task).order_by(asc(Task.title)) 
        else:
            tasks_list = db.session.query(Task).order_by(desc(Task.title)) 
    
    else:
        tasks_list = Task.query.all()
    
    task_response = [] 
    for task in tasks_list:
        task_response.append(task.to_json_no_key())
    
    return jsonify(task_response), 200


@task_list_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):
    
    if not is_int(task_id):
        return {
            "message": "id must be an integer",
            "success": False
        },400
    
    task = Task.query.get(task_id)
    
    if task == None:
        return Response("",status=404)
    
    if task:
        return task.to_json(), 200
    
    return {
        "message": f"Task with id {task_id} was not found",
        "success": False
    }, 404 

#wave 2 : sort the tasks by ascending and descending order
#when getting all tasks, and using query params, the value of sort is not "desc" or "asc"?
    
@task_list_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    
    task = Task.query.get(task_id)
    
    if task == None:
        return Response("", status=404)
    
    if not task:
        return Response("", status=404)
    
    if task: 
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return task.to_json(), 200

@task_list_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)    
def delete_single_task(task_id):

    task = Task.query.get(task_id)

    if task == None:
        return Response("", status=404)

    if task:
        db.session.delete(task)
        db.session.commit()
        
        task_details = f"Task {task.task_id} \"{task.title}\" successfully deleted"
        
        return jsonify(details=task_details
                         ),200
    

#WAVE 3 Mark Complete on a Completed Task , Mark Complete on a Completed Task
@task_list_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)    
def patch_single_task(task_id):
    
    if not is_int(task_id):
        #return Response("",status=404)
        return {
            "message": "id must be an integer",
            "success": False
        },400
    
    
    task = Task.query.get(task_id)
    
    if task == None:
        return Response("", status=404)
    
    task.completed_at = date.today()
    task.is_complete = True
    #form_data = request.get_json()
    task.title = task.title #Wave 4

    
    db.session.commit()
    
    return task.to_json(), 200


# WAVE 3 Mark Incomplete on an Incompleted Task , Mark Incomplete on an Incompleted Task
@task_list_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)    
def patch_task_incomplete(task_id):
    
    if not is_int(task_id):
        #return Response("",status=404)
        return {
            "message": "id must be an integer",
            "success": False
        },400 

    
    task = Task.query.get(task_id)
    
    if task == None:
        return Response("", status=404)
    
    if task.completed_at is not None:
        task.completed_at = None
        task.is_complete = False
    
    db.session.commit()
    
    return task.to_json(), 200

#WAVE 5 - CRUD goal 
#create new blueprint for goal
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_a_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return jsonify(details="Invalid data"),400
    
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()
    
    return new_goal.to_json_goal(), 201


@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_goals():
    
    goal_list = Goal.query.all()
    
    goal_response = [] 
    for goal in goal_list:
        goal_response.append(goal.to_json_goal_no_key())
    
    return jsonify(goal_response), 200

@goals_bp.route("<goal_id>", methods=["GET"], strict_slashes=False)
def get_one_goal(goal_id):
    
    if not is_int(goal_id):
        return {
            "message": "id must be an integer",
            "success": False
        },400
        
    goal = Goal.query.get(goal_id)
    
    if goal == None:
        return Response("",status=404)
    
    if goal:
        return goal.to_json_goal(), 200
    
 
@goals_bp.route("<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):
    
    goal = Goal.query.get(goal_id)
    
    if goal == None:
        return Response("", status=404)
    
    if not goal:
        return Response("", status=404)
    
    if goal: 
        form_data = request.get_json()

        goal.title = form_data["title"]

        db.session.commit()

        return goal.to_json_goal(), 200

@goals_bp.route("<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal == None:
        return Response("", status=404)

    if goal:
        db.session.delete(goal)
        db.session.commit()
        
        goal_details = f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        
        return jsonify(details=goal_details
                         ),200