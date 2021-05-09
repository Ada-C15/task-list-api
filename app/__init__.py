from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os # This built-in module provides a way to read environment variables
from dotenv import load_dotenv # The python-dotenv package specifies to import the package like this

db = SQLAlchemy()
migrate = Migrate()
load_dotenv() # The python-dotenv package specifies to call this method, which loads the values from our .env file so that the os module is able to see them.

def create_app(test_config=None):  # We have called the new parameter test_config which should receive a dictionary of configuration settings. It has a default value of None, making the param optional.
    app = Flask(__name__) 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# the connection string to connect the database to Flask is located in .env
    if test_config is None:
# Check the keyword argument test_config. When we call create_app(), if test_config is falsy (None or empty), that means we are not trying to run the app in a test environment.
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else: # If there is a test_config passed in, this means we're trying to test the app, which can have special test settings
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")   
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal
    # ^^Make task and goal visible to flask migration helper

    from .routes import tasks_bp
    app.register_blueprint(tasks_bp)

    from .routes import goals_bp
    app.register_blueprint(goals_bp)
    # ^^ Register Blueprints here

    return app
