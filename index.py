from ast import Global
import re
from threading import currentThread
from tkinter.tix import INTEGER

from numpy import may_share_memory
import detectHuman
from flask import render_template, request, redirect, session, jsonify, Flask, Response, flash, url_for
from flask_admin.base import Admin
from importlib_metadata import method_cache
from sqlalchemy import util
from sqlalchemy.sql.functions import user
from __init__ import app, camera, cv2
# from admin import*
# from models import Users
from flask_login import login_user, logout_user
# import utils
import math
import os
from werkzeug.utils import secure_filename
from detectHuman import detect, DSIZE_FRAME
from recognition import recognition


count_1 = 0
maxCount_1 = 0
value = 0.5
names = set()


def generate_frames(value = 0.5):
    global count_1, maxCount_1
    while True:
    # read the camera frame
        success,frame = camera.read()
        if not success:
            break
        else:
            frame, count, maxCount = detect(frame, ['person'], value)
            count_1 = count
            maxCount_1 = maxCount

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



def generate_frames1():
    global names
    while True:
    # read the camera frame
        success,frame = camera.read()
        if not success:
            break
        else:
            frame, names = recognition(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route("/upload-rate", methods = ["POST"])
# def uploadRate():
#     value = request.form.get("value")

@app.route("/api/get-name", methods = ["POST"])
def getName():
    myArray = []
    for var in names:
        myArray.append({
            'name' : var
        })
    return jsonify(myArray)

@app.route("/api/update-count", methods = ["POST"]) 
def updateCount():
    
    return jsonify({
        "count" : count_1,
        "maxCount" : maxCount_1
    })

@app.route("/", methods = ["POST"])
def uploadValue():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    else:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_video filename: ' + filename)
        flash('Video successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)


@app.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
    if filename != 'temp.mp4':
        fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
        out = cv2.VideoWriter("static/upload/temp.mp4", fourcc, 5.0, DSIZE_FRAME)
        detectHuman.detectByPathVideo('static/upload/' + filename,out)

    return redirect(url_for('static', filename='upload/temp.mp4'), code=301)

@app.route("/") 
def home():     
    return render_template('index.html')  

@app.route("/video")
def video():
    return Response(generate_frames(0.5),
            mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route("/video2")
def video2():
    return Response(generate_frames1(),
            mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True)