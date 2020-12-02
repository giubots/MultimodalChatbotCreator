from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def helloWorld():
	if request.method == 'GET' \
				and request.args != {}:
		return request.args
	else:
		return 'Hello World!'