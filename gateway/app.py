from flask import Flask,request,send_file
import os, gridfs, pika, json
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storageAPI import utility
from bson.objectid import ObjectId
app = Flask(__name__)

#Initialise the Mongo Connections for separate databases
mongo_video_connection=PyMongo(app, uri='mongodb://host.minikube.internal:27017/videos')
mongo_audio_connection=PyMongo( app, uri='mongodb://host.minikube.internal:27017/mp3s')

fs_videos = gridfs.GridFS(mongo_video_connection.db)
fs_mp3s = gridfs.GridFS(mongo_audio_connection.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@app.route("/login", methods=['POST'])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err

@app.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    access = json.loads(access)
    
    if err:
        return err

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exactly 1 file per request", 400

        for _, f in request.files.items():
            err = utility.upload(f, fs_videos, channel, access)

            if err:
                return err

        return "success!", 200

    else:
        return "Unauthorised", 403

@app.route("/download", methods=["POST"])
def download():
    access,err = validate.token(request)
    access = json.loads(access)

    if err:
        return err

    if access["admin"]:
        fid_string = request.args.get("file_id")
        if not fid_string:
            return "file_id required", 400
        try:
            output = fs_mp3s.get(ObjectId(fid_string))
            return send_file(output, download_name=f'{fid_string}.mp3')
        except Exception as err:
            print(err)
            return "Internal Server Error", 500

    return "Unauthorised", 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
