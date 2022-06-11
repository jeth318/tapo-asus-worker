from flask import Flask, jsonify, request, make_response
from dotenv import load_dotenv
import os
from tapo_integration import dispatchPrivacyToggle

load_dotenv()
app = Flask(__name__)
port = os.environ["PORT"]
host = os.environ["HOST"]

@app.route('/privacy', methods=['POST'])
def index():
    message = ""

    try:
        state = request.json["privacy"]
        if state == 1:
            dispatchPrivacyToggle("on")
            message = "activating privacy mode"
        elif state == 0:
            dispatchPrivacyToggle("off")
            message = "deactivating privacy mode"
        else:
            message = "Privacy value invalid. Must me an integer 1/0 or boolean true/false"
            return make_response(buildErrorResponse(message), 400)
    except Exception as e:
        message = "Something here didn't go as planned. " + str(e)
        return make_response(buildErrorResponse(message), 500)

    return make_response(buildResponse(message), 200)


def buildResponse(message):
    return jsonify(
        success=1,
        message="Initiated command: " + message
    )


def buildErrorResponse(message):
    return jsonify(
        success=0,
        message=message
    )


app.run(host="localhost", port=port)
