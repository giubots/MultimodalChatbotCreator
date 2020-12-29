from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json

# import framework
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'framework'))
from framework import Framework
from parameters import *

app = Flask(__name__)
api = Api(app)


# create REST backup API
# https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f
class Event(Resource):
    def get(self):
        return {'response': 'ok'}, 200
    def post(self):
        # https://stackoverflow.com/questions/30491841/python-flask-restful-post-not-taking-json-arguments
        recv = request.get_json(force=True)
        print(recv)
        # initialize framework
        my_framework = Framework(Process([Activity("start", "echo", ActivityType.START),
                                          Activity("echo", "end", ActivityType.TASK),
                                          Activity("end", None, ActivityType.END)],
                                         "start"), {"end": "Process completed!"}, {}, c_getter, my_nlu)
        my_framework.handle_text_input('')
        if recv['type'] == 'utterance':
            send = my_framework.handle_text_input(recv['utterance'])
            return send  # no need to convert to string on rest
                         # (vs Websockets)
        else:
            send = my_framework.handle_data_input(recv['payload'])
            return send


api.add_resource(Event, '/event')


if __name__ == '__main__':
    app.run()  # run our Flask app for the REST API on port 5000