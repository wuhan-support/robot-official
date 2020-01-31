from .config import *
from .robot_app import app


def start_app():
    app.run(ROBOT_HOST, port=ROBOT_PORT)