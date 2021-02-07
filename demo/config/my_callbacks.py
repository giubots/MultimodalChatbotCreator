from mmcc_framework import CTX_COMPLETED, NoNluAdapter, Response

nluAdapter = NoNluAdapter([])


def payload_enabled_items(context: dict, state: str, action: str = ""):
    """

    :param context: to send useful info about the state of the framework
    :param state: the state is the state it's coming from
    :param action: the action performed in the state
    :return: what to show in the frontend ui to the user, given the last interaction
    """

    info = {}
    if (  # choose_info is 1
            (state == "customize" and action == "skip") or
            (state == "change_info" and action != "end") or
            action == "change_info"
    ):
        info = {
            "last_address": context["address"],
            "last_payment": context["details"]
        }
    elif (state == "choose_item" or # choose_customize is 1
          state in ["select_size", "select_color"] or
          (state == "customize" and action != "skip")):
        info = {
            "item": context["item"],
        }
    elif action == "end":  # complete is 1
        info = {
            "item": context["item"],
            "size": context["size"],
            "color": context["color"],
            "address": context["address"],
            "payment": context["details"]
        }

    return {
        "useful_variables": info,
        "show_items": int(state == "start"),  # [enable user to] select items to buy
        "choose_customize": int(
            state == "choose_item" or
            state in ["select_size", "select_color"] or
            (state == "customize" and action != "skip")
        ),  # [] choose to change size or color
        "show_size": int(state == "customize" and action == "size"),  # [] change size
        "show_color": int(state == "customize" and action == "color"),  # [] change color
        "custom_completed": int(  # this means if we have selected size and we already have the color, and vice versa
            (state == "select_size" and action == "color") or
            (state == "select_color" and action == "size")
        ),  # [] proceed to choose info when he clicks on continue (because both color/size has already been chosen)
        # so the user can choose go to change info
        "choose_info": int(  # this means that he went from customize to here (clicking continue)
            (state == "customize" and action == "skip") or
            (state == "change_info" and action != "end") or
            action == "change_info"
        ),  # [] choose to change address or payment info
        "show_address": int(state == "change_info" and action == "address"),
        "show_payment": int(state == "change_info" and action == "payment"),
        "complete": int(action == "end")
    }


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
    print(context)
    return Response(kb, context, True, utterance=kb["start"],
                    payload=payload_enabled_items(context, "start"))


def choose_item(data, kb, context):
    if data["intent"] == "state_preference":
        if "preference" in data and data["preference"] in kb["items"]:
            context["item"] = data["preference"]
            return Response(kb, context, True,
                            payload=payload_enabled_items(context, "choose_item"))
        return Response(kb, context, False, utterance=kb["wrong_item"],
                        payload=payload_enabled_items(context, "start"))
    return Response(kb, context, False, utterance=handle_other(data, kb),
                    payload=payload_enabled_items(context, "start"))


def customize(data, kb, context):
    if data["intent"] == "change_something":
        if "change" in data and data["change"] == "size":
            return Response(kb, context, True, choice="select_size",
                            payload=payload_enabled_items(context,
                                                          "customize",
                                                          "size"
                                                          ))
        if "change" in data and data["change"] == "color":
            return Response(kb, context, True, choice="select_color",
                            payload=payload_enabled_items(context,
                                                          "customize",
                                                          "color"
                                                          ))
        return Response(kb, context, False, utterance=kb["wrong_customize"],
                        payload=payload_enabled_items(context, "choose_item"))
    if data["intent"] == "change_nothing" or data["intent"] == "deny":
        if "customize" in context[CTX_COMPLETED]:
            return Response(kb, context, True, choice=None,
                            payload=payload_enabled_items(context, "customize", "skip"))
        return Response(kb, context, False, utterance=kb["wrong_customize"],
                        payload=payload_enabled_items(context, "choose_item"))
    return Response(kb, context, False, utterance=handle_other(data, kb),
                    payload=payload_enabled_items(context, "choose_item"))


def select_size(data, kb, context):
    if data["intent"] == "state_preference":
        if "preference" in data and data["preference"] in kb["sizes"]:
            context["size"] = data["preference"]
            return Response(kb, context, True,
                            payload=payload_enabled_items(context, "select_size", "color" if "color" in context else ""))
        return Response(kb, context, False, utterance=kb["wrong_size"],
                        payload=payload_enabled_items(context, "customize", "size"))
    return Response(kb, context, False, utterance=handle_other(data, kb),
                    payload=payload_enabled_items(context, "customize", "size"))


def select_color(data, kb, context):
    if data["intent"] == "state_preference":
        if "preference" in data and data["preference"] in kb["colors"]:
            context["color"] = data["preference"]
            # if we have the size, then we can proceed with the process
            return Response(kb, context, True,
                            payload=payload_enabled_items(context, "select_color", "size" if "size" in context else ""))
        return Response(kb, context, False, utterance=kb["wrong_color"],
                        payload=payload_enabled_items(context, "customize", "color"))
    return Response(kb, context, False, utterance=handle_other(data, kb),
                    payload=payload_enabled_items(context, "customize", "color"))


def change_info(data, kb, context):
    if data["intent"] == "change_something":
        if "change" in data and data["change"] == "address":
            return Response(kb, context, True, choice="change_address",
                            payload=payload_enabled_items(context, "change_info", "address"))
        if "change" in data and data["change"] == "payment":
            return Response(kb, context, True, choice="change_payment",
                            payload=payload_enabled_items(context, "change_info", "payment"))
        return Response(kb, context, False, utterance=kb["wrong_change"])
    if data["intent"] == "change_nothing" or data["intent"] == "deny":
        return Response(kb, context, True, choice=None, utterance=final_recap(context),
                        payload=payload_enabled_items(context, "change_info", "end"))
    return Response(kb, context, False, utterance=handle_other(data, kb),
                    payload=payload_enabled_items(context, "change_info", "change_info"))


def change_address(data, kb, context):
    if data["intent"] == "give_address":
        if "address" in data:
            context["address"] = data["address"]
            kb["last_address"] = data["address"]
            return Response(kb, context, True,
                            payload=payload_enabled_items(context, "change_address", "change_info"))
        return Response(kb, context, False, utterance=kb["address_error"],
                        payload=payload_enabled_items(context, "change_address", "change_info"))
    return Response(kb, context, False, utterance=handle_other(data, kb),
                    payload=payload_enabled_items(context, "change_address", "change_info"))


def change_payment(data, kb, context):
    if data["intent"] == "payment_details":
        if "details" in data:
            context["details"] = data["details"]
            kb["last_payment"] = data["details"]
            return Response(kb, context, True,
                            payload=payload_enabled_items(context, "change_payment", "change_info"))
        return Response(kb, context, False, utterance=kb["payment_error"],
                        payload=payload_enabled_items(context, "change_payment", "change_info"))
    return Response(kb, context, False, utterance=handle_other(data, kb),
                    payload=payload_enabled_items(context, "change_payment", "change_info"))


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
