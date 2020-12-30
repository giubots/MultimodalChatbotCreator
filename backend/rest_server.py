from flask import Flask, request, session
from flask_restful import Resource, Api, reqparse
import json

# import framework
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'framework'))
from framework import Framework
from parameters import *

app = Flask(__name__)
api = Api(app)

my_framework = dict()

# create REST backup API
# https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f

class Init(Resource):
    def post(self):
        if 'uid' in session:
            return {'error': 'Session already initialized.'}
        # get argument uid, uid is the user id
        parser = reqparse.RequestParser()
        parser.add_argument('uid', required=True)
        args = parser.parse_args()
        uid = args['uid']
        # session.save(uid)
        session['uid'] = uid
        print(session)
        # initialize framework
        # TODO: the process will be sent from the client
        my_framework['uid'] = Framework(Process([Activity("start", "echo", ActivityType.START),
                                          Activity("echo", "end", ActivityType.TASK),
                                          Activity("end", None, ActivityType.END)],
                                         "start"), {"end": "Process completed!"}, {}, c_getter, my_nlu)
        my_framework['uid'].handle_text_input('')
        return {'response': f'your uid is: {uid}'}, 200


api.add_resource(Init, '/init')


class Event(Resource):
    # check if session is active (i.e. if there is an session_id set)
    # def get(self):
    #     return {'response': 'ok'}, 200

    def post(self):
        if 'uid' in session:
            uid = session.get('uid')
        else:
            print(session)
            return {'error': 'The user has not been initialized yet'}
        # https://stackoverflow.com/questions/30491841/python-flask-restful-post-not-taking-json-arguments
        recv = request.get_json(force=True)
        print(recv)
        if recv['type'] == 'utterance':
            send = my_framework['uid'].handle_text_input(recv['utterance'])
            return send  # no need to convert to string on rest
                         # (vs Websockets)
        else:
            send = my_framework['uid'].handle_data_input(recv['payload'])
            return send


api.add_resource(Event, '/event')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()  # run our Flask app for the REST API on port 5000