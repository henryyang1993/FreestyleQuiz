from flask import Flask, request


app = Flask(__name__, static_url_path='')

@app.route("/index", methods=['GET'])
def handleIndex():
    return "ok"


@app.route("/song", methods=['GET'])
def handleSong():
    test = request.args.get('test')
    return test


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80, threaded=True)
    
