from app import db
from .models.task import Task
from flask import request, Blueprint, make_response, jsonify, Response

task_list_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_list_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()
    
    if (Task.title not in new_task) or (Task.description not in new_task) or task.completed_at not in new_task:
        return make_response(jsonify("details : Invalid data"))
    
    task_completed = Task.compute_completed_at()
    
    if task_completed == False:
        return make_response("task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": False 
        }), 201
    else:    
        return make_response(jsonify(new_task, 201)
     #Optional enhancement : when creating a task, the value of completed_at is a string that is not a datetime?                        

@task_list_bp.route("/tasks", methods=["GET"], strict_slashes=False)
def tasks():
    
    tasks_list = []
    
    task_filter = request.args.get("completed_at")
    
    if task_filter is not None:
        task_title = task_filter
        tasks_list = Task.query.filter_by(completed_at=None) 
    else:
        task_list = Task.query.all()
    
    task_response = [] 
    for task in tasks_list:
        task_response.append(task.to_json())
    return jsonify(task_response), 200


@task_list_bp.route("/tasks", methods=["GET"], strict_slashes=False)
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

''' #wave 2 : sort the tasks by ascending and descending order
#when getting all tasks, and using query params, the value of sort is not "desc" or "asc"?
@task_list_bp.route("/tasks", methods=["GET"], strict_slashes=False)
def get_tasks_asc(title):
    tasks_list = []
    
    task_filter_asc = sessions.query(Tasks).order_by(Tasks.title.asc()).all()
    task_filter_desc = sessions.query(Tasks).order_by(Tasks.title.desc()).all()
    
    if task_filter_asc:
        return  '''
    
@task_list_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    
    task = Task.query.get(task_id)
    
    if task == None:
        return Response("", status=404)
    
     if not task :
        return Response("", status=404)
    
    if task: 
        form_data = request.get_json()

        task.name = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return Response(f"Task #{task.id} successfully updated", status=200)

@task_list_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)    
def delete_single_task(task_id):

    task = Task.query.get(task_id)

    if task == None:
        return Response("", status=404)

    if task:
        db.session.delete(task)
        db.session.commit()
        return Response(f"details : Task {task.id}  {task.title} successfully deleted")
        
#WAVE 3 PATCH REQUEST MARK COMPLETE ON INCOMPLETE TASK
#WAVE 3 PATCH REQUESR MARCH INCOMPLETE ON COMPLETE TASK
#WAVE 3 PATCH REQUESR MARCH COMPLETE ON COMPLETE TASK
#WAVE 3 PATCH REQUESR MARCH INCOMPLETE ON INCOMPLETE TASK
#WAVE 3 PATCH MARCK COMPLETE AND INCOMPLETE ON MISSING TASK



#WAVE 5 - CRUD goal 
#create new blueprint for goal
