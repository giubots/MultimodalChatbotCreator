import requests

# create a Session
s = requests.Session()

name = 'My Name'

print(f'> /init?name={name}')
greeting = s.post(
  url='http://127.0.0.1:5000/init',
  data={
    'uid': name
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

print(f'> /event: {event}')
response = s.post(
  url='http://127.0.0.1:5000/event',
  json=event
)
print(f'< {response.json()}')
