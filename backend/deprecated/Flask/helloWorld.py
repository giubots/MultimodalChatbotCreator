from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketIO = SocketIO(app)


@app.route('/', methods=['GET'])
def helloWorld():
	if request.method == 'GET' \
				and request.args != {}:
		return request.args
	else:
		return 'Hello World!'


if __name__ == '__main__':
	socketIO.run(app)