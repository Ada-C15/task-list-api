
from app import db
from app.models.task import Task

from flask import request, Blueprint, make_response

# Blueprint instance - groups routes that start with /tasks.
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# START HERE============================
# @blueprint_name.route("/endpoint/path/here", methods=["GET"])
# def endpoint_name():
#     my_beautiful_response_body = "Hello, World!"
#     return my_beautiful_response_body