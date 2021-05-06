from app.models.task import Task
from app import db
from flask import request, Blueprint, make_response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_single_task(task_id):

    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None),404

    if request.method == "GET":
        return {"task": task.get_resp()}, 200

    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return {"task": task.get_resp()}, 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({
            "details":f'Task {task.task_id} "{task.title}" successfully deleted'
        }), 200


@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        # if sort_query:
        #     tasks = Task.query.order_by(f"title {sort_query}")
        if sort_query == 'asc':
            tasks = Task.query.order_by(Task.title.asc())
        elif sort_query == 'desc':
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.all()
        
        task_response = []
        for task in tasks:
            task_response.append(task.get_resp())
        return make_response(jsonify(task_response), 200)
    
    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return jsonify({"details":"Invalid data"}), 400

        else:
            new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()
        return make_response(jsonify({"task": new_task.get_resp()}), 201)

