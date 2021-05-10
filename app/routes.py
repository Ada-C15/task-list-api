from app import db
from app.models.task import Task, to_dict
from flask import Blueprint, request, make_response, jsonify


tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    request_body = request.get_json()

    response = {"details": "Invalid data"}

    if "title" not in request_body.keys() or "description" not in request_body.keys() or "completed_at" not in request_body.keys():

        return jsonify(response), 400

    else:
        new_task = Task(title = request_body["title"], description = request_body["description"], completed_at = request_body["completed_at"])
        db.session.add(new_task)
        db.session.commit()
        valid_task = {"task": to_dict(new_task)}

        return jsonify(valid_task), 201


# @tasks_bp.route("/tasks?sort=asc", methods=["GET"])
# def asc_tasks_sort(tasks):
#     tasks = Task.query.all()
#     tasks_response = []

#     if tasks is None:
#         return jsonify(tasks_response)
    
#     else:
#         for task in tasks:
#             tasks_response.append(to_dict(task))
        
#         sorted_list = sorted(tasks_response, key=lambda x: (x["title"])) 

#         return jsonify(sorted_list)



@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    tasks_response = []

    if tasks is None:
        return jsonify(tasks_response)
    
    else:
        for task in tasks:
            tasks_response.append(to_dict(task))

        return jsonify(tasks_response)


@tasks_bp.route("/tasks/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):

    task = Task.query.get(task_id)

    if request.method == "GET":
        if task is None:
            return make_response(f"404 Not Found", 404) 

        else:
            one_task = to_dict(task)

            return {"task": one_task}


    elif request.method == "PUT":
        if task: 
            form_data = request.get_json()
            task.title = form_data["title"]
            task.description = form_data["description"]
            task.is_complete = form_data["completed_at"]
            db.session.commit()

            updated_task = {
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": bool(task.completed_at)
            }
        else: 
            return make_response(f"", 404) 
           
        return {'task': updated_task}

    elif request.method == "DELETE":
        if task:
            db.session.delete(task)
            db.session.commit()

            response = {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}

            return jsonify(response), 200
        
        else:
            return make_response(f"", 404)


# @tasks_bp.route("/tasks/<task_id>/mark_complete", methods=["PATCH"])
# def mark_complete(task):

#     request_body = request.get_json()
#     complete_task = Task(title = request_body["title"], description = request_body["description"], completed_at = request_body["completed_at"])

    
#     mark_task_complete = {
#             "id": complete_task.task_id,
#             "title": complete_task.title,
#             "description": complete_task.description,
#             "is_complete": True
#     }

#     return {"task": mark_task_complete}


# @tasks_bp.route("/tasks/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task):
#     request_body = request.get_json()
#     incomplete_task = Task(title = request_body["title"], description = request_body["description"], completed_at = request_body["completed_at"])

    
#     mark_task_incomplete = {
#             "id": incomplete_task.task_id,
#             "title": incomplete_task.title,
#             "description": incomplete_task.description,
#             "is_complete": False
#     }

#     return {"task": mark_task_incomplete}

# comment 
