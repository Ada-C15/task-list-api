from app import db
from flask import Blueprint
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
