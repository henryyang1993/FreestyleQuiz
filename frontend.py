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

    welcome_msg = render_template('welcome')

    return statement(welcome_msg)

@ask.intent("SongIntent")

def songMode():
    audioData = requests.get("http://localhost/track").json()
    session.attributes['answer'] = audioData['song']
    session.attributes['song'] = audioData['song']
    session.attributes['singer'] = audioData['singer']
    
    audio = {
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": audioData['preview_url'],
                            "url": audioData['preview_url'],
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
    session.attributes['answer'] = audioData['singer']
    session.attributes['song'] = audioData['song']
    session.attributes['singer'] = audioData['singer']
    
    audio = {
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": audioData['preview_url'],
                            "url": audioData['preview_url'],
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

@ask.intent("nextIntent")

def next_round():
    msg = render_template('next')
    return question(msg)
 

@ask.intent("AnswerIntent", convert={'answer': str})

def answer(answer):
    correct_answer = session.attributes['answer']
    song = session.attributes['song']
    singer = session.attributes['singer']

    if answer.lower() == correct_answer.lower():

        msg = render_template('correct', song=song, singer=singer)

    else:

        msg = render_template('wrong', song=song, singer=singer)

    return question(msg)


if __name__ == '__main__':

    app.run(debug=True)