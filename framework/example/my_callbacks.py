# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo
from framework import Response


def get_callback(activity_id: str):
    return _my_callbacks[activity_id]


def start(data, kb, context):
    return Response(kb, context, True, payload={"BA": True, "BB": False, "FC": False, "FC_c": ""})


def insert_name(data, kb, context):
    if "name" in data and data["name"] != "":
        context["name"] = data["name"]
        return Response(kb, context, True, payload={"BA": False, "BB": True})
    return Response(kb, context, False, utterance=kb["insert_name_err"])


def insert_age(data, kb, context):
    if "age" in data:
        try:
            age = int(data["age"])
            if age < kb["insert_age_old"]:
                context["age"] = data["age"]
                return Response(kb, context, True, utterance=f'{context["name"]} {context["age"]}',
                                payload={"BB": False, "FC": True, "FC_c": context["name"] + " " + context["age"]})
        except ValueError:
            pass
    return Response(kb, context, False, utterance=kb["insert_age_err"])


_my_callbacks = {
    "start": start,
    "insert_name": insert_name,
    "insert_age": insert_age,
}
