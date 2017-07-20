from flask import Flask, request
import requests
import base64
import json

app = Flask(__name__, static_url_path="")
spotify = {}

with open("spotify.txt") as f:
    spotify = json.loads(f.read())


def getToken():
    client_id = spotify["CLIENT_ID"]
    client_credentials = spotify["CLIENT_CREDENTIALS"]
    header = client_id + ":" + client_credentials
    r = requests.post("https://accounts.spotify.com/api/token", 
        data = {"grant_type":"client_credentials"},
        headers = {"Authorization": "Basic " + base64.b64encode(header.encode()).decode()})
    response = r.json()
    return response["access_token"]


@app.route("/index", methods=["GET"])
def handleIndex():
    return "ok"


@app.route("/track", methods=["GET"])
def handleSong():
    meta = request.args.get("meta")
    token = getToken()
    r = requests.get("https://api.spotify.com/v1/tracks/2TpxZ7JUBn3uw46aR7qd6V", 
        headers = {"Authorization": "Bearer " + token})
    response = r.json()
    data = ""
    if meta == "song":
        data = response["name"]
    if meta == "artist":
        data = response["artists"][0]["name"]
    if meta == "album":
        data = response["album"]["name"]
    ret = {"preview": response["preview_url"], "meta": data}
    return json.dumps(ret)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80, threaded=True)
    
