from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None): # change the test_config value if you want to load test tasks/goals to the test db you created
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # addresses arbitrary and unexplained warning that you dont need to worry about

    if test_config is None: # loads results of API calls to 'real' db
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True # loads results of test API calls to the testing db you built
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal
    from .routes import task_bp # also import blueprint instances from routes file; access needed to register below
    from .routes import goal_bp

    db.init_app(app) # start up the application
    migrate.init_app(app, db) # prep dbs/ start up their connection to application

    # Register Blueprints here
    app.register_blueprint(task_bp) # register blueprints imported above; cant say more than that; flask docs dont help..? check w Vishaal for more info!
    app.register_blueprint(goal_bp)

    return app
