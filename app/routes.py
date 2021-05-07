from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id" : task.task_id,
                "title" : task.title,
                "description" : task.description,
                "is_complete" : task.is_complete
            })

        return jsonify(tasks_response)

    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_task = Task(title=request_body["title"],
                            description=request_body["description"],
                            completed_at=request_body["completed_at"]
                            )
        except KeyError:
            return make_response({"details": "Invalid data"}, 400)

        db.session.add(new_task)
        db.session.commit()

        return make_response({
            "task" : {
                "id" : new_task.task_id,
                "title" : new_task.title,
                "description" : new_task.description,
                "is_complete" : new_task.is_complete
            }
        }, 201)


@tasks_bp.route("/<active_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(active_id):
    task = Task.query.get_or_404(active_id)

    if request.method == "GET":
        return {
            "task" : {
                "id" : task.task_id,
                "title" : task.title,
                "description" : task.description,
                "is_complete" : task.is_complete
            }
        }

    elif request.method == "PUT":
        update_data = request.get_json()

        task.title = update_data["title"]
        task.description = update_data["description"]
        task.completed_at = update_data["completed_at"]

        db.session.commit()

        return {
            "task" : {
                "id" : task.task_id,
                "title" : task.title,
                "description" : task.description,
                "is_complete" : task.is_complete
            }
        }

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"})
