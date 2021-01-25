from mmcc_framework import Response


def start(data, kb, context):
    return Response(kb, context, True, payload={"show_name": False, "show_age": False, "show_choose_name": True,
                                                "show_choose_nickname": True, "show_field": False,
                                                "field_contents": ""})


def insert_name(data, kb, context):
    if "name" in data and data["name"] != "":
        context["name"] = data["name"]
        return Response(kb, context, True, payload={"show_name": False, "show_age": True})
    return Response(kb, context, False, utterance=kb["insert_name_err"])


def insert_nickname(data, kb, context):
    if "nickname" in data and data["nickname"] != "":
        context["nickname"] = data["nickname"]
        return Response(kb, context, True, payload={"show_name": False, "show_age": True})
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
                                payload={"show_age": False, "show_field": True,
                                         "field_contents": name + " " + context["age"]})
        except ValueError:
            pass
    return Response(kb, context, False, utterance=kb["insert_age_err"])


def name_nickname(data, kb, context):
    if "name_nickname" in data:
        if data["name_nickname"] == "name":
            return Response(kb, context, True, choice="insert_name",
                            payload={"show_choose_name": False, "show_choose_nickname": False, "show_name": True})
        if data["name_nickname"] == "nickname":
            return Response(kb, context, True, choice="insert_nickname",
                            payload={"show_choose_name": False, "show_choose_nickname": False})
    return Response(kb, context, False, utterance=kb["wrong_choice"])


def get_callback(activity_id: str):
    """ Given an activity id, this returns the callback corresponding to that activity. """
    return _my_callbacks[activity_id]


_my_callbacks = {
    "start": start,
    "name_nickname": name_nickname,
    "insert_name": insert_name,
    "insert_nickname": insert_nickname,
    "insert_age": insert_age,
}
