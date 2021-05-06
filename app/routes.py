from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from .models.task import Task
from .models.goal import Goal
from app import db 
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


#wave_1
@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    if not "title" in request_body or not "description" in request_body or not "completed_at" in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400
    else: 
        task = Task(title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"])

    db.session.add(task)
    db.session.commit()

    return {
            "task": task.to_json()
        }, 201

# def is_completed(request_body):
#     if "completed_at" in request_body:
#         is_complete = True 
#     return is_complete

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    #sort title by ace and desc order
    #check wave_2 tests
    sort_by_title = request.args.get("sort")
    if sort_by_title == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_by_title == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response)


#GET PUT DELETE 
@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    elif request.method == "GET":
        return make_response({"task": task.to_json()}, 200)

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return make_response(
            {"task": task.to_json()
        }, 200)

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
            })

#wave_3 
#creating custom endpoints with is_complete: True or False
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"]) #update
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if not task:
        return ("", 404)

    task.completed_at = datetime.now()
    task.is_complete = True 
    # task.is_complete()


    #db.session.add(task)
    db.session.commit()

    # return make_response({
    #     "message": f"Task {task.title} has been marked complete"
    #     })

    return {
        "task": task.to_json()
        }, 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"]) #update
def mark_incomplete(task_id):

    task = Task.query.get(task_id)
    if not task:
        return ("", 404)

    if task.completed_at != None:
       task.completed_at = None
       task.is_complete = False 
    
    db.session.commit()

    # return make_response({
    #     "message": f"Task {task.title} has been marked incomplete"
    #     })

    return {
        "task": task.to_json()
        }, 200








#wave_4
#use external Web API - slack 


#wave_5
#created second models for goals
@goals_bp.route("", methods=["POST"])
def create_goals():
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400
    new_goal = Goal(title=request_body["title"])

    di.session.add(new_goal)
    db.session.commit()

    return {
        "goal":new_goal()
    }, 200






# Wave 6
# Establishing a One-to-Many Relationship



#optional- deployment

#enhacements




