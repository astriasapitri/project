import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    SOCKETIO_MESSAGE_QUEUE = None
    SENSOR_API_KEY = os.getenv('SENSOR_API_KEY', 'smartfit-secret')
