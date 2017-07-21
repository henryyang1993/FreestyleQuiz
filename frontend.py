import logging

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

@ask.intent("ModeIntent", convert={'mode': str})

def selectMode(mode):
    session.attributes['mode'] = mode
    #play music
    # play_msg = render_template('guess')
    music = {
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": "0",
                            "url": "https://p.scdn.co/mp3-preview/12b8cee72118f995f5494e1b34251e4ac997445e?cid=1cc6b53b0b124bd2bb767bdcafc1b471",
                            "offsetInMilliseconds": 0
                        }
                    }
                }
            ],
            "shouldEndSession": False
        }
    }
    session.attributes['answer'] = "singer"
    return music
    # return statement(play_msg)


@ask.intent("YesIntent")

def next_round():
    mode = session.attributes['mode']
    selectMode(mode)
 

@ask.intent("AnswerIntent", convert={'answer': str})

def answer(answer):

    winning_answer = session.attributes['answer']

    if answer == winning_answer:

        msg = render_template('win')

    else:

        msg = render_template('lose')

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)