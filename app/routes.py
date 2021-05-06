from flask import Blueprint
from app import db
from .models.task import Task
from flask import request, jsonify, make_response

task_list_bp = Blueprint("tasks", __name__, url_prefix="/tasks")