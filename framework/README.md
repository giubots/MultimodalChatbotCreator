# MULTIMODAL CHATBOT CREATOR - FRAMEWORK

This project is based on the paper "A Conceptual Framework for Multi-modal Process-driven Conversational
Agents" [WIP LINK]. It provides a framework that, if kept updated with the inputs from the user, guides him through an
appropriately defined process, regardless of the input type. More info are available at [WIP PRESENTATION].
___

# Usage

See the full example on how this framework can be used. [WIP EXAMPLE].

A developer that wants to use this framework has to:

* Provide a process description
* Provide a set of callbacks
* Provide a "knowledge base"
* Provide a "context"
* Create a `Framework` object
* Call `handle_text_input` or `handle_data_input` whenever an input from the user is received
* Display back to the user the `Response` returned by the methods.

To create a `Framework` it is possible to provide some json files with the process description, context and knowledge
base, while the callbacks are provided through a function (more info below):

```Python
from framework import Framework

my_framework = Framework.from_file(open("my_process.json"),
                                   open("my_kb.json"),
                                   open("my_context.json"),
                                   get_callback,
                                   nlu)

```

### The knowledge base and the context:

These are dictionaries with key-value pairs.

```json
{
  "insert_name": "Please insert your name"
}
```

SPECIAL KB KEYS: When a task is starting, the framework **automatically** searches in the knowledge base a value
corresponding to its id and appends its value to the utterance in the `Response`. For example, when a task called "
insert_name" starts, the message in the knowledge base of the example above will be put in the utterance. If you prefer
to handle manually all the utterances, avoid using the id of a task as a knowledge base key.

SPECIAL CONTEXT KEYS: In the context, the framework **automatically** adds a `CTX_COMPLETED` key whose value is a list
of task id that can be accessed by the developer in the callbacks: if a gateway (activity with type PARALLEL or OR) is
in this list then it is completed, and the user can move to the next activity. For example when the user has chosen all
the tasks in a PARALLEL activity with the id "my_par", `context[CTX_COMPLETED]` will contain "my_par".

### The process description:

A `Process` object represents the sequence of actions the user can perform: it contains a set of `Activity` objects and
the id of the first activity.

Each `Activity` corresponds to an input from the user, and has:

* A unique id
* The id of the next activity
* A `type`
* Some choices, depending on the `type`

The process can have a single starting point and multiple END, each id must be unique.

The choices are a list containing the id of each of the first activities in a gateway (OR, XOR or PARALLEL) block. The
last task in a block has `null` as next. For example, if the process contains a XOR that allows to execute (A then B)
XOR C, and then finally D, the corresponding description would be:

```json
{
  "activities": [
    {
      "my_id": "start",
      "next_id": "myXOR",
      "my_type": "START"
    },
    {
      "my_id": "myXOR",
      "next_id": "D",
      "my_type": "XOR",
      "choices": [
        "A",
        "C"
      ]
    },
    {
      "my_id": "A",
      "next_id": "B",
      "my_type": "TASK"
    },
    {
      "my_id": "B",
      "next_id": null,
      "my_type": "TASK"
    },
    {
      "my_id": "C",
      "next_id": null,
      "my_type": "TASK"
    },
    {
      "my_id": "D",
      "next_id": "end",
      "my_type": "TASK"
    },
    {
      "my_id": "end",
      "next_id": null,
      "my_type": "END"
    }
  ],
  "first_activity_id": "start"
}
```

### The callbacks and the responses:

Each `Activity` has an associated callback that is in charge of:

* Handling the input
* Updating the knowledge base
* Updating the context
* Returning a `Response` with the updated knowledge base and context
* The response also can contain an utterance and a payload that are returned by `handle_text_input`
  or `handle_data_input`
* Finally, the Response specifies whether the activity is completed and an optional "choice", depending on the type.

```Python
from framework import Response


def callback(data, kb, context) -> Response:
    # Obtain my_choice from the data, evaluate it and prepare my_payload.
    my_choice = ...
    completed = ...
    my_payload = ...
    ...
    if completed:
        return Response(kb, context, True, payload=my_payload, choice=my_choice)
    return Response(kb, context, False, utterance=kb["my_kb_key"])

```

The example above is a callback that could be associated with a OR, XOR or PARALLEL activity. If the user inserted a
valid choice then it is completed and returns the choice, otherwise it returns an utterance from the knowledge base.

To pass the callbacks to the `Framework`, provide a method that, given the id of the task, returns the correct callback
(without running it).

When `handle_text_input` or `handle_data_input` terminate, they return a data structure that contains the utterance and
the payload.

### The types of activities:

There are six `Type` values:

* TASK: Represents the operations to be done to complete the process, the callback returns true if the user can move on
  to the next activity.
* START: It is the entry point of the process, its callback must return always `True` and can be used to prepare the
  state using the payload.
* END: A "sink" state, that represents the termination of the process.
* PARALLEL: A task that gives some options to the user, the user can chose which one to execute, and is completed when
  all have been chosen at least once. Its callback must return the id of the chosen activity if the user input was
  valid.
* XOR: Similar to a PARALLEL, but allows the user to choose exactly one of the options.
* OR: Similar to a PARALLEL, but it is completed when the user has chosen at least one of the options.