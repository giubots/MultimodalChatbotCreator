import string
import random
import os.path
from threading import Lock
from urllib.parse import urlsplit, parse_qsl, urlencode
from mmcc_framework import Framework
from config.my_callbacks import get_callback, nluAdapter
from uuid import uuid4

lock = Lock()


def id_generator(
			size=24,
			chars=string.ascii_letters + string.digits + string.punctuation
):
	return ''.join(random.choice(chars) for _ in range(size))


def uuid_generator():
	return str(uuid4())


def get_params(url):
	# print(get_params('/?uid=My%20Name'))
	# returns {'uid': 'My Name'}
	query = urlsplit(url).query
	return dict(parse_qsl(query))


def add_params(url, params: dict):
	# print(add_params("ws://localhost:8765", {'uid': 'My Name'}))
	# returns {'uid': 'My Name'}
	return url + '?' + urlencode(params)


def create_framework():
    # TODO: framework personalized for each user (Tutor)
    # Prepare the state and the framework.
    return Framework.from_file(os.path.join("config", "my_process.json"),
                               os.path.join("config", "my_kb.json"),
                               {},
                               get_callback,
                               nluAdapter,
                               lock
                               )


def welcome_message_framework(framework):
	return framework.handle_text_input('')
