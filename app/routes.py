from app import db
from app.models.task import Task
from flask import request, Blueprint, jsonify, Response, make_response

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def post_tasks():
    request_body = request.get_json()
    
    if "title" in request_body.keys() and "description" in request_body.keys() and "completed_at" in request_body.keys() :
        task = Task(title=request_body["title"],
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"],
                    )
    
        db.session.add(task)
        db.session.commit()

        return jsonify({"task": task.api_response()}), 201

    else:
        return make_response(
            {"details": "Invalid data"
            }
        ), 400



@tasks_bp.route("", methods=["GET"])
def get_tasks():

    title_query = request.args.get("sort")
    if title_query == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.api_response())

    return jsonify(tasks_response), 200

#filter
# Q1=Task.query.filter(db)....
# Q1.order_by(...)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response(jsonify(None), 404)
        # return make_response("",404)
        # return Response(None),404
        # return jsonify(None), 404

    return jsonify({"task": task.api_response()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def put_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return Response(None),404

    form_data = request.get_json()

    task.title = form_data["title"]
    task.description = form_data["description"]
    task.completed_at = form_data["completed_at"]

    db.session.commit()

    return jsonify({"task": task.api_response()}), 200 

@tasks_bp.route("/<task_id>", methods=["PATCH"])
def patch_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return Response(None),404

    form_data = request.get_json()

    # task.title = form_data["title"]
    # task.description = form_data["description"]
    task.completed_at = True

    db.session.commit()
 
    return jsonify(task.api_response()), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return Response(None),404

    db.session.delete(task)
    db.session.commit()
    return make_response(
        {"details": f'Task {task.id} "{task.title}" successfully deleted'
        }
    ), 200