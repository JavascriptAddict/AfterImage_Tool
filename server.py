from flask import Flask, render_template, jsonify, request
import config
import utils
import threading

app = Flask(__name__, static_url_path='', 
            static_folder='public/static',
            template_folder='public/templates')

ATTACKSLOCK = threading.Lock()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/proxies')
def proxies():
    data = dict()
    data["proxies"] = [proxy.__dict__ for proxy in config.PROXIES.proxyList]
    return jsonify(data)

@app.route('/attacksawait')
def attacksawait():
    data = config.ATTACKSAWAIT
    return jsonify(data)

@app.route('/attacks')
def attacks():
    data = config.ATTACKS
    return jsonify(data)

@app.route('/test', methods=["GET", "POST"])
def test():
    # Simple test
    uid = request.args.get("uid")
    ATTACKSLOCK.acquire()
    dictIndex = utils.getAwaitIndexByKey(uid)
    config.ATTACKSAWAIT["attacks"][dictIndex]["attack"] = True
    ATTACKSLOCK.release()
    state = {"state": 200, "message": "Success"}
    return jsonify(state)