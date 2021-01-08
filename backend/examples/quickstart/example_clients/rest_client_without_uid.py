import requests

# create a Session
s = requests.Session()

print(f'> /get_uid')
uid = s.get(url='http://127.0.0.1:5000/get_uid').json()
print(f'< Your uid: {uid}')

print(f'> /init?uid={uid}')
greeting = s.post(
  url='http://127.0.0.1:5000/init',
  data={
    'uid': uid
  }
)
print(f'< {greeting.json()}')


event_utterance = {
  'type': 'utterance',
  'utterance': 'my_utterance'  # this is an example text
}

event_data = {
  'type': 'data',
  'payload': {
    'echo': 'Bob'  # this is an example data
  }
}

# switch between test utterance or data
event = event_data

for i in range(2):
  print(f'> /event: {event}')
  greeting = s.post(
    url='http://127.0.0.1:5000/event',
    json=event
  )
  print(f'< {greeting.json()}')
