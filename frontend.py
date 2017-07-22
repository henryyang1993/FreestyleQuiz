import logging
import json
import requests


from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_game():

    welcome_msg = render_template("welcome")

    return question(welcome_msg).reprompt(render_template("reprompt"))


@ask.intent("GameIntent")

def gameMode():
    audioData = requests.get("http://localhost:8081/songMeta").json()
    session.attributes["song"] = audioData["song"]
    session.attributes["singer"] = audioData["singer"]
    ssml = "<speak>Guess the song name! <audio src='{}' />Aho, you miss that! Are you ready for next round?</speak>".format("https://b530e54b.ngrok.io/songfile?name=%s" % audioData["song"].replace(" ", "_"))

    audio = {
        "response": {
            "outputSpeech": {
                "type": "SSML",
                "ssml": ssml
            },
            "shouldEndSession": False
        },
        "sessionAttributes":session.attributes
    }
    return json.dumps(audio)


@ask.intent("TerminateIntent")

def terminate():
    msg = render_template("terminate")
    return statement(msg)

 
@ask.intent("NextIntent")

def next_round():
    msg = render_template("next")
    return question(msg).reprompt(render_template("reprompt"))
 

@ask.intent("AnswerIntent", convert={"song": str})

def answer(song):
    correct_song = session.attributes["song"]
    correct_singer = session.attributes["singer"]

    if song.lower() == correct_song.lower():

        msg = render_template("correct", song=correct_song, singer=correct_singer)

    else:

        msg = render_template("wrong", song=correct_song, singer=correct_singer)

    return question(msg).reprompt(render_template("reprompt"))


@ask.intent("ListenIntent")

def listenMode():
    audioData = requests.get("http://localhost:8081/fullSongMeta").json()
    url = "https://b530e54b.ngrok.io/songfile?name=%s" % audioData["song"].replace(" ", "_")

    audio = {
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": url,
                            "url": url,
                            "offsetInMilliseconds": 0
                        }
                    }
                }
            ],
            "shouldEndSession": True
        }
    }
    return json.dumps(audio)


@ask.intent("AMAZON.CancelIntent")

def cancelAlexa():
    return stopAlexa()


@ask.intent("AMAZON.StopIntent")

def stopAlexa():
    audio = {
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Stop"
                }
            ],
            "shouldEndSession": True
        }
    }
    return json.dumps(audio)


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=8080, threaded=True)