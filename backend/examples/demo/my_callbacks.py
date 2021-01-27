from mmcc_framework import CTX_COMPLETED, NoNluAdapter, Response

nluAdapter = NoNluAdapter([])


def handle_other(data, kb):
    if data["intent"] == "greet":
        return kb["start"]
    if data["intent"] == "bot_challenge":
        return kb["bot_challenge"]
    return kb["not_understand"]


def final_recap(context):
    return f'You chose: {context["item"]}, size: {context["size"]}, color: {context["color"]}. \n' \
           f'Deliver to: {context["address"]}, pay with: {context["details"]}'


def start(data, kb, context):
    context["address"] = kb["last_address"]
    context["details"] = kb["last_payment"]
    return Response(kb, context, True, utterance=kb["start"])


def choose_item(data, kb, context):
    if data["intent"] == "state_preference":
        print(kb["items"])
        if "preference" in data and data["preference"] in kb["items"]:
            context["item"] = data["preference"]
            return Response(kb, context, True)
        return Response(kb, context, False, utterance=kb["wrong_item"])
    return Response(kb, context, False, utterance=handle_other(data, kb))


def customize(data, kb, context):
    if data["intent"] == "change_something":
        if "change" in data and data["change"] == "size":
            return Response(kb, context, True, choice="select_size")
        if "change" in data and data["change"] == "color":
            return Response(kb, context, True, choice="select_color")
        return Response(kb, context, False, utterance=kb["wrong_customize"])
    if data["intent"] == "change_nothing" or data["intent"] == "deny":
        if "customize" in context[CTX_COMPLETED]:
            return Response(kb, context, True, choice=None)
        return Response(kb, context, False, utterance=kb["wrong_customize"])
    return Response(kb, context, False, utterance=handle_other(data, kb))


def select_color(data, kb, context):
    if data["intent"] == "state_preference":
        if "preference" in data and data["preference"].lower() in kb["colors"]:
            context["color"] = data["preference"]
            return Response(kb, context, True)
        return Response(kb, context, False, utterance=kb["wrong_color"])
    return Response(kb, context, False, utterance=handle_other(data, kb))


def select_size(data, kb, context):
    if data["intent"] == "state_preference":
        if "preference" in data and data["preference"].lower() in kb["sizes"]:
            context["size"] = data["preference"]
            return Response(kb, context, True)
        return Response(kb, context, False, utterance=kb["wrong_size"])
    return Response(kb, context, False, utterance=handle_other(data, kb))


def change_info(data, kb, context):
    if data["intent"] == "change_something":
        if "change" in data and data["change"] == "address":
            return Response(kb, context, True, choice="change_address")
        if "change" in data and data["change"] == "details":
            return Response(kb, context, True, choice="change_payment")
        return Response(kb, context, False, utterance=kb["wrong_change"])
    if data["intent"] == "change_nothing" or data["intent"] == "deny":
        return Response(kb, context, True, choice=None, utterance=final_recap(context))
    return Response(kb, context, False, utterance=handle_other(data, kb))


def change_address(data, kb, context):
    if data["intent"] == "give_address":
        if "address" in data:
            context["address"] = data["address"]
            kb["last_address"] = data["address"]
            return Response(kb, context, True)
        return Response(kb, context, False, utterance=kb["address_error"])
    return Response(kb, context, False, utterance=handle_other(data, kb))


def change_payment(data, kb, context):
    if data["intent"] == "payment_details":
        if "details" in data:
            context["details"] = data["details"]
            kb["last_payment"] = data["payment"]
            return Response(kb, context, True)
        return Response(kb, context, False, utterance=kb["payment_error"])
    return Response(kb, context, False, utterance=handle_other(data, kb))


def get_callback(activity_id: str):
    """ Given an activity id, this returns the callback corresponding to that activity. """
    return _my_callbacks[activity_id]


_my_callbacks = {
    "start": start,
    "choose_item": choose_item,
    "customize": customize,
    "select_color": select_color,
    "select_size": select_size,
    "change_info": change_info,
    "change_address": change_address,
    "change_payment": change_payment,
}
