import os
from datetime import datetime
from flask import Blueprint, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc

from app import db
from app.models.task import Task



task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

index_bp= Blueprint("index", __name__, url_prefix="/")


@index_bp.route("", methods=["GET"])
def index():  #html homepage = index
    return make_response({"name": "Hello index2"}, 200)

@task_bp.route("", methods=["GET"])
def task():  #html homepage = index
    tasks = Task.query.all()
    task_response = []

    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title).all()

    if request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    
    for task in tasks:
        task_response.append(task.to_json())

    return jsonify(task_response), 200


@task_bp.route("/<int:id>", methods=["GET"])
def get_task(id):  #html homepage = index
    task = Task.query.filter_by(task_id=id).first()
    if task == None:
        return make_response(f"Task {id} not found", 404)
    else:
        return jsonify({"task":task.to_json()}), 200

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:

        t = Task(title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"])
    except KeyError:
        return make_response({
            "details": "Invalid data"
        }, 400)

    db.session.add(t)
    db.session.commit()
    return {
        "task": t.to_json()
    }, 201

@task_bp.route("/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get(id)
    if task == None:
        return make_response(f"Task {id} not found", 404)
    else:
        update_body = request.get_json()
        task.title = update_body["title"]
        task.description = update_body["description"]
        db.session.commit()
        return make_response({"task":task.to_json()}, 200)

@task_bp.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get(id)
    if task == None:
        return make_response(f"Task {id} not found", 404)
    else:
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f"Task {id} \"{task.title}\" successfully deleted"}, 200)

@task_bp.route("/<int:id>/mark_complete", methods=["PATCH"])
def complete_task(id):
    task = Task.query.get(id)
    if task == None:
        return make_response(f"Task {id} not found", 404)
    else:
        task.completed_at = datetime.now()
        db.session.commit()
        return make_response({"task":task.to_json()}, 200)

@task_bp.route("/<int:id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(id):
    task = Task.query.get(id)
    if task == None:
        return make_response(f"Task {id} not found", 404)
    else:
        task.completed_at = None
        db.session.commit()
        return make_response({"task":task.to_json()}, 200)