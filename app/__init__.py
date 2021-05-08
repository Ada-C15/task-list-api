from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None: #not test_config vs test_config=None
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    ## this all grabs my models, where my routes are and my blueprints  to 
    ## be able to run my app  #grabbing it all from everywhere to be able to run my app

    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal
    from .routes import task_bp # ADDED THIS, uncomment and run db upgrade when routes done
    from .routes import goal_bp  # ADDED THIS

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here   
    app.register_blueprint(task_bp)  # ADDED THIS: need to create blue prints yet but they'll go here
    app.register_blueprint(goal_bp)  # same as above

    # IF ALL GOES WELL, HERE YOU APP IS READY TO work and do posts! gets, deletes, etc!
    return app
