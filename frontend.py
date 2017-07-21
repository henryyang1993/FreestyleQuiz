import logging
import json
import requests

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)

@ask.intent("SongIntent")

def songMode():
    # session.attributes['mode'] = "song"
    musicData = requests.get("http://localhost/track?meta=song").json()
    session.attributes['answer'] = musicData['meta']
    print "Get Meta Answer: " + musicData['meta']

    audio = {
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": "0",
                            "url": musicData['preview'],
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
    # session.attributes['mode'] = "singer"
    #play music
    # play_msg = render_template('guess')
    musicData = requests.get("http://localhost/track?meta=artist").json()
    session.attributes['answer'] = musicData['meta']
    print "Get Meta Answer: " + musicData['meta']
    audio = {
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": "0",
                            "url": musicData['preview'],
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

@ask.intent("YesIntent")

def next_round():
    msg = render_template('mode')
    return statement(msg)
 

@ask.intent("AnswerIntent", convert={'answer': str})

def answer(answer):
    print "The answer is " + answer
    winning_answer = session.attributes['answer']

    if answer == winning_answer:

        msg = render_template('win')

    else:

        msg = render_template('lose')

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)