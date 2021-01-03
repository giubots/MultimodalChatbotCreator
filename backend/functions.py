import string
import random
from urllib.parse import urlsplit, parse_qsl


def id_generator(
	size=24,
	chars=string.ascii_letters + string.digits + string.punctuation
):
	return ''.join(random.choice(chars) for _ in range(size))


def parse_url(url):
	# print(parse_url('/?uid=My%20Name'))
	# returns {'uid': 'My Name'}
	query = urlsplit(url).query
	return dict(parse_qsl(query))
