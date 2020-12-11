from flask import Flask, jsonify, make_response, request
import api
import json
import flask_cors
import os


class App(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        flask_cors.CORS(self)

app = App(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
@app.route('/index')
def index():
    return jsonify('Hello')


@app.route('/api/v1/get_started', methods=['GET', 'OPTIONS', 'POST'])
def start():
    if request.method == 'OPTIONS':
        return build_preflight_response()
    return api.get_messages(messenger)


@app.route('/api/v1/get_all', methods=['GET', 'OPTIONS'])
def get_all_messages():
    if request.method == 'OPTIONS':
        return build_preflight_response()
    return jsonify(api.get_messages(messenger))


@app.route('/api/v1/delete', methods=['DELETE', 'OPTIONS'])
def delete():
    if request.method == 'OPTIONS':
        return build_preflight_response()
    return jsonify(api.delete_message(messenger, json.loads(request.data.decode())))


@app.route('/api/v1/create_or_update', methods=['POST', 'OPTIONS'])
def create_or_update():
    if request.method == 'OPTIONS':
        return build_preflight_response()
    return jsonify(api.add_or_update_message(messenger, json.loads(request.data.decode())))
    
#app.run()


messenger = api.init_messenger()


def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


# Bind to PORT if defined, otherwise default to 5000.
app.run()
