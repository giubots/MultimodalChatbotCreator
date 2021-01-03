import string
import random
from urllib.parse import urlsplit, parse_qsl, urlencode


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
