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


@ask.intent("SongIntent")

def songMode():
    audioData = requests.get("http://localhost/track").json()
    session.attributes["mode"] = "song"
    session.attributes["answer"] = audioData["song"]
    session.attributes["song"] = audioData["song"]
    session.attributes["singer"] = audioData["singer"]
    
    audio = {
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": audioData["preview_url"],
                            "url": audioData["preview_url"],
                            "offsetInMilliseconds": 0
                        }
                    }
                }
            ],
            "shouldEndSession": False
        },
        "sessionAttributes":session.attributes
    }
    return json.dumps(audio)


@ask.intent("SingerIntent")

def singerMode():
    audioData = requests.get("http://localhost/track").json()
    session.attributes["mode"] = "singer"
    session.attributes["answer"] = audioData["singer"]
    session.attributes["song"] = audioData["song"]
    session.attributes["singer"] = audioData["singer"]
    
    audio = {
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": audioData["preview_url"],
                            "url": audioData["preview_url"],
                            "offsetInMilliseconds": 0
                        }
                    }
                }
            ],
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
 

@ask.intent("AnswerIntent", convert={"song": str, "singer": str})

def answer(song, singer):
    correct_mode = session.attributes["mode"]
    correct_answer = session.attributes["answer"]
    correct_song = session.attributes["song"]
    correct_singer = session.attributes["singer"]

    if correct_mode == "song":
        answer = song
    else:
        answer = singer

    if answer and answer.lower() == correct_answer.lower():

        msg = render_template("correct", song=correct_song, singer=correct_singer)

    else:

        msg = render_template("wrong", song=correct_song, singer=correct_singer)

    return question(msg).reprompt(render_template("reprompt"))


if __name__ == "__main__":

    app.run(debug=True)