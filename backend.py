from flask import Flask, request, send_from_directory
import requests
import base64
import json
import random


app = Flask(__name__, static_url_path="")


def getSong():
    with open("SongsList.json", 'r') as songs_file:
        songs_array = json.load(songs_file)
        index = random.randint(0, 2)
        return songs_array[index]


def getFullSong():
    with open("FullSongsList.json", 'r') as songs_file:
        songs_array = json.load(songs_file)
        index = random.randint(0, 2)
        return songs_array[index]


@app.route("/songfile", methods=["GET"])
def getSongFile():
    songname = request.args.get('name', 'sugar')
    return send_from_directory('music', "%s.mp3" % songname)


@app.route("/songMeta", methods=["GET"])
def getSongMeta():
    ret = getSong()
    return json.dumps(ret)


@app.route("/fullSongMeta", methods=["GET"])
def getFullSongMeta():
    ret = getFullSong()
    return json.dumps(ret)

	
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081, threaded=True)
    
