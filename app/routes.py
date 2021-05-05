from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify

tasks_bp = Blueprint("tasks",__name__,url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def handle_tasks():

    request_body = request.get_json()
    

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body: 
        return ({
            "details":"Invalid data"
        },400)
    else:
        task = Task(title=request_body["title"],

                    description=request_body["description"],
                    completed_at =request_body["completed_at"])
        db.session.add(task)
        db.session.commit()

        return make_response({"task":task.to_json()
                
                },201)

def is_completed_or_no(request_body):
    
    is_complete = False
    if request_body["completed_at"]:
        is_complete = True
    return is_complete
    
@tasks_bp.route("", methods=["GET"])
def get_all_task():
    title_sort_query = request.args.get("sort")
    
    if title_sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif title_sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    else:
        tasks = Task.query.all()
        
    tasks_response = []
    for task in tasks:
            tasks_response.append(task.to_json())
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET","PUT","DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response(" ", 404)
    if request.method == "GET":
        return make_response({"task":
           task.to_json()
        
        },200)
    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
    
        db.session.commit()
        return make_response({"task":
                task.to_json()
            
            },200)
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({
                    "details": f'Task {task.task_id} "{task.title}" successfully deleted'
                })

