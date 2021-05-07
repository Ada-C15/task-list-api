from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])

def tasks():

    tasks = Task.query.all()
    tasks_response = []
    if request.method == "GET":
        # tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
            })
            # tasks_response.append(task.to_json())
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        
        # Invalid task if missing title, description, or completed_at     
        if "completed_at" not in request_body or "description" not in request_body or "title" not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        else:
            new_task =  Task(
                title = request_body["title"],
                description = request_body["description"],
                completed_at = request_body["completed_at"])
            tasks_response.append(new_task)
    # if tasks is None:
    #     return jsonify(tasks_response), 200

    # add this model to the database. Commit these changes and make it happen
            db.session.add(new_task)
            db.session.commit()

            return jsonify(tasks_response), 201

@tasks_bp.route("/<task_id>", methods=["GET","PUT","DELETE"], strict_slashes=False)
def handle_task(task_id):

    # Find the task with the given id
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
        # return make_response(jsonify(None), 404)

    if request.method == "GET": 
        # return make_response(jsonify("task": {
        # "id": task_id,
        # "title": task.title,
        # "description": task.description,
        # "is_complete": True if task.completed_at else False
        # }), 200)
        return jsonify(task=task.as_dict())
    

    elif request.method == "PUT":
        new_data = request.get_json()

        task.title = new_data["title"]
        task.description = new_data["description"]
        task.completed_at = new_data["completed_at"]

        db.session.commit()

        return make_response(jsonify(task=task.as_dict()), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()

        # return make_response(f"details: Task{task.id} {task.title} successfully deleted")
        return make_response(jsonify(details=f"Task {task.id} \"{task.title}\" successfully deleted"), 200)
    

