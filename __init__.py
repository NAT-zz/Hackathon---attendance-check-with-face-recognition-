from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import cloudinary
import cv2

camera = cv2.VideoCapture(0)
app = Flask(__name__)

app.secret_key = "213sad23"
app.config['UPLOAD_FOLDER'] = 'static/upload/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

