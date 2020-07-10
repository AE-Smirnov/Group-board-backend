from flask import Flask, jsonify, make_response, request
import api
import json
import flask_cors


class App(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        flask_cors.CORS(self)

if __name__ == '__main__':
    app = App(__name__)
    app.config['JSON_AS_ASCII'] = False


@app.route('/')
@app.route('/index')
def index():
    return jsonify('Hello')


@app.route('/api/v1/get_all', methods=['GET'])
def get_all():
    return str(api.get_all(timetable)).replace("'", '"')


@app.route('/api/v1/create_or_update', methods=['POST', 'OPTIONS'])
def add_lesson():
    if request.method == 'OPTIONS':
        return build_preflight_response()
    return jsonify(api.add_lesson(timetable, json.loads(request.data.decode())))


@app.route('/api/v1/delete', methods=['DELETE', 'OPTIONS'])
def delete_lesson():
    if request.method == 'OPTIONS':
        return build_preflight_response()
    return jsonify(api.delete_lesson(timetable, json.loads(request.data.decode())))


timetable = api.init_timetable()


def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


app.run()
