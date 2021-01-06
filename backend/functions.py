import string
import random
from threading import Lock
from urllib.parse import urlsplit, parse_qsl, urlencode
from mccreator_framework.framework import Framework
from mccreator_framework.nlu_adapters import NoNluAdapter
from config.my_callbacks import get_callback, noNluList

lock = Lock()


def id_generator(
			size=24,
			chars=string.ascii_letters + string.digits + string.punctuation
):
	return ''.join(random.choice(chars) for _ in range(size))


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
	# self.state = {"show_name": False, "show_age": False, "show_choose_name": True, "show_choose_nickname": True,
	#               "show_field": False, "field_contents": ""}
	return Framework.from_file("config/my_process.json",
														"config/my_kb.json",
														{},
														get_callback,
														NoNluAdapter(noNluList),
														lock
	)


def welcome_message_framework(framework):
	return framework.handle_text_input('')
