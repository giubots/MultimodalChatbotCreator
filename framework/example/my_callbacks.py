# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo
from framework import Response


def get_callback(activity_id: str):
    return _my_callbacks[activity_id]


def start(data, kb, context):
    return Response(kb, context, True,
                    payload={"BA": False, "BB": False, "BC": True, "BD": True, "FC": False, "FC_c": ""})


def insert_name(data, kb, context):
    if "name" in data and data["name"] != "":
        context["name"] = data["name"]
        return Response(kb, context, True, payload={"BA": False, "BB": True})
    return Response(kb, context, False, utterance=kb["insert_name_err"])


def insert_nickname(data, kb, context):
    if "nickname" in data and data["nickname"] != "":
        context["nickname"] = data["nickname"]
        return Response(kb, context, True, payload={"BA": False, "BB": True})
    return Response(kb, context, False, utterance=kb["insert_nickname_err"])


def insert_age(data, kb, context):
    if "age" in data:
        try:
            age = int(data["age"])
            if age < kb["insert_age_old"]:
                context["age"] = data["age"]
                if "name" in context:
                    name = "Name, " + context["name"]
                else:
                    name = "Nickname, " + context["nickname"]
                return Response(kb, context, True, utterance=f'{name} {context["age"]}',
                                payload={"BB": False, "FC": True, "FC_c": name + " " + context["age"]})
        except ValueError:
            pass
    return Response(kb, context, False, utterance=kb["insert_age_err"])


def name_nickname(data, kb, context):
    if "name_nickname" in data:
        if data["name_nickname"] == "name":
            return Response(kb, context, True, choice="insert_name", payload={"BC": False, "BD": False, "BA": True})
        if data["name_nickname"] == "nickname":
            return Response(kb, context, True, choice="insert_nickname", payload={"BC": False, "BD": False})
        return Response(kb, context, False, utterance=kb["wrong_choice"])


_my_callbacks = {
    "start": start,
    "name_nickname": name_nickname,
    "insert_name": insert_name,
    "insert_nickname": insert_nickname,
    "insert_age": insert_age,
}
