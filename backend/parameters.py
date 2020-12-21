# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo

# Example:
# my_input = {
#     "type": "utterance / data",
#     "utterance": "my utterance", # my_framework.handle_text_input(my_input["utterance"])
#     "payload": {...}             # my_framework.handle_data_input({...})
# }


from framework import *


def start_c(data, kb, context):
    return Response(kb, context, True, utterance="Ready", payload={"echo": "Ready"})


def echo_c(data, kb, context):
    if "echo" in data:
        my_echo = f'Framework says: {data["echo"]}'
        return Response(kb, context, True, utterance=my_echo, payload={"echo": my_echo})
    return Response(kb, context, False, utterance="Error! Payload is the data received.", payload=data)


def c_getter(key):
    if key == "start":
        return start_c
    if key == "echo":
        return echo_c
    raise KeyError(key)


def my_nlu(string):
    return {"echo": string}


my_framework = Framework(Process([Activity("start", "echo", ActivityType.START),
                                  Activity("echo", "end", ActivityType.TASK),
                                  Activity("end", None, ActivityType.END)],
                                 "start"), {"end": "Process completed!"}, {}, c_getter, my_nlu)
