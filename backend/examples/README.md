# MULTIMODAL CHATBOT CREATOR - BACKEND EXAMPLES

To run the examples, copy and paste all the files of the example you want to run in the [config folder](../config)

Go back to the [backend guide](../README.md)
___

## Example 1: Quickstart

[comment]: <> (TODO: We need to add example pics)

This is as simple as it gets! It's a single interaction with the chatbot, and the chatbot will reply with what you said to him. So it will do an echo.

### How to start it

* Move [my_callbacks.py](quickstart/my_callbacks.py), [my_kb.json](quickstart/my_kb.json), and [my_process.json](quickstart/my_process.json) to the [config](../config) folder
* Run the [rest_server](../rest_server.py) or the [websocket_server](../websocket_server.py)
* Run one of the [example_clients](quickstart/example_clients/) to learn how to perform the connection in a real web client.
* Run the [frontend](../../frontend/README.md) to see how it works in a simple chatbot web app.
* Adapt your website to handle the connection just like the example clients do.
* You are ready to move on to the next example, Name Nickname!

### Example Clients

#### Simple Rest Client
[rest_client.py](quickstart/example_clients/rest_client.py) is made to work with the Quickstart example, and it sends a post request with uid in the body (to identify the user) to `/init`

Then if `event` is set to `event_data`, it will send a data input (such as a click of a button).

If it's set to `event_utterance` instead, it will send a text from the user (for example sent in the chat of the website).

It will receive the response of the Framework.

#### Rest Client, but with the uid generated from the server
[rest_client_without_uid.py](quickstart/example_clients/rest_client_without_uid.py)

This example is similar to the one above, but it does an additional request to `/get_id` at the beginning, to get the uid from the server. It then proceeds in the same way as the simple rest client above.



## Example 2: Name Nickname

This is a more complete example:

The process now resembles a real conversation. It first asks if you want a name or a surname, then it asks you to insert it, and finally it asks for your age and stops.

You can see the process we described in [my_process.json](name_nickname/my_process.json).

[my_kb.json](name_nickname/my_kb.json) contains the phrases that the framework must say when in an activity inside the process/interaction.

[my_callbacks.py](name_nickname/my_callbacks.py) describes how the process works, and must contain:
* The `Response` object from the framework
```python
from mccreator_framework.framework import Response
```
* The list of names to give to the Natural Language Understanding
```python
noNluList = ["name", "nickname", "age", "name_nickname"]
```

[comment]: <> (TODO: explain better noNluList)

* A function for each `Activity` of the process
```python
def start(data, kb, context):
    return Response(kb, context, True, payload={"show_name": False, "show_age": False, "show_choose_name": True,
                                                "show_choose_nickname": True, "show_field": False,
                                                "field_contents": ""})


def insert_name(data, kb, context):
    if "name" in data and data["name"] != "":
        context["name"] = data["name"]
        return Response(kb, context, True, payload={"show_name": False, "show_age": True})
    return Response(kb, context, False, utterance=kb["insert_name_err"])
```

[comment]: <> (TODO: explain better the callback functions, how to create them)


* The `get_callback(activity_id)` function along with a dictionary of the functions to pass to the `Framework` based on which Activity the Process is in.
```python
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
```


