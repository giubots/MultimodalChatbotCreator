from mccreator_framework.framework import Response

noNluList = ["echo"]

def start_c(data, kb, context):
	return Response(kb, context, True, utterance="Ready", payload={"echo": "Ready"})


def echo_c(data, kb, context):
	if "echo" in data:
		my_echo = f'Framework says: {data["echo"]}'
		return Response(kb, context, True, utterance=my_echo, payload={"echo": my_echo})
	return Response(kb, context, False, utterance="Error! Payload is the data received.", payload=data)


def get_callback(activity_id: str):
	""" Given an activity id, this returns the callback corresponding to that activity. """
	return _my_callbacks[activity_id]


_my_callbacks = {
	"start": start_c,
	"echo": echo_c
}
