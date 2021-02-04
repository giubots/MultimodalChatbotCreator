# MULTIMODAL CHATBOT CREATOR - FRAMEWORK

This project is based on the paper "A Conceptual Framework for Multi-modal Process-driven Conversational Agents".
It provides a framework that, if kept updated with the inputs from the user, guides him through an appropriately defined process, regardless of the input type.

This is the core component that implements the logic of the framework, you can use it in a standalone application;
if instead you are interested in a React implementation, take a look at the [backend](../backend/README.md) and [frontend](../frontend/src/react-mmcc/README.md).

# Installation

To use the framework in a python application, run
`pip install 'git+https://github.com/giubots/MultimodalChatbotCreator@main#egg=mmcc-framework&subdirectory=framework'`

# Usage

There are two examples that show how to use the framework with a simple Tkinter application.
The [basic example](./examples/basic/README.md) uses a `NoNluAdapter`, meaning no NLU is performed;
the [rasa example](./examples/rasa/README.md) uses [Rasa](https://rasa.com/).
To use Rasa you will have to install it, or use [Docker](https://www.docker.com/).

A developer that wants to use this framework has to:

1) Provide a [process description](#the-process-description)
1) Provide a set of [callbacks](#the-callbacks-and-the-responses)
1) Provide a [knowledge base](#the-knowledge-base-and-the-context)
1) Provide a [context](#the-knowledge-base-and-the-context)
1) Choose a [NluAdapter](#the-nlu-adapter)
1) Create a [Framework](#the-framework) object
1) Call `handle_text_input` or `handle_data_input` whenever an input from the user is received
1) Display back to the user the contents of the `Response` returned by the methods.

If you plan to use the provided backend, you just have to provide the first three and the NLU.

### The Framework

To create a `Framework` it is possible to provide some files with the process description in json format, context and
knowledge base, while the callbacks are provided through a function (more info below):

```Python
from mmcc_framework import Framework, RasaNlu

framework = Framework.from_file("my_process.json",
                                "my_kb.json",
                                {},  # Notice that in this case the context does not use a file.
                                callback_getter,  # This is a function that given an activity id returns its callback.
                                RasaNlu())
```

When the framework is called with `handle_data_input` the provided data is passed to the callback corresponding to the
current activity, obtained with the `callback_getter` function. When the framework is called with `handle_text_input`,
the given text is transformed into data by the chosen `NluAdapter`, and the data is passed to the callback.

The callbacks can use the data and what is contained in the kb and context to produce a `Response`. The response can
contain an utterance and a payload that are returned to the caller. You are free to use the payload as you prefer, the
data that you provide instead depends on the `NluAdapter`
that you chose.

If multiple instances share the same files, remember to provide a unique lock shared by all the instances, this will
allow the framework to handle concurrency when using the files.

If you prefer to create a framework instance from some existing data structure you can use Framework's constructor, and
you will have to provide also a callback that will be invoked when it will be time to save the kb.

### The process description

A `Process` object represents the sequence of actions the user can perform, it is divided in steps called activities.
Each activity corresponds to an input from the user. The framework starts its execution from an initial activity, and
moves on to the following ones based on the response of the callback corresponding to the current activity.

The process must have a single starting point and can have multiple END activities.

Each activity has a unique id, the id of the next activity and a type.

Depending on the type, an activity can also provide some choices, these consist in a list containing the id of each of
the first activities in a gateway (OR, XOR or PARALLEL) block. The last task in a block has `None` as next.

If an activity A is part of a bigger activity B (for example A's id is in B's choices list), A can have `None` as its
next id to indicate that the framework must go to B (or, if B is of type XOR, to B's next).

For example, if the process contains a XOR that allows to execute (A then B) XOR C, and then finally D, the
corresponding description would be:

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

There are six `ActivityType` values:

- TASK: Represents an operation to be done to complete the process, the callback response contains true if the user can
  move on to the next activity.
- START: It is the entry point of the process, its response must contain True and can be used to prepare the state using
  the payload.
- END: A "sink" state that represents the termination of the process.
- PARALLEL: A task that gives some options to the user, the user can choose which one to execute, and is completed when
  all have been chosen at least once. Its callback must return the id of the chosen activity if the user input was
  valid, `None` to move on to the next task.
- XOR: Similar to a PARALLEL, but allows the user to choose exactly one of the options.
- OR: Similar to a PARALLEL, but it is completed when the user has chosen at least one of the options.

### The callbacks and the responses

Each `Activity` (END excluded) has an associated callback that is in charge of:

- Handling the input
- Updating the knowledge base
- Updating the context
- Returning a `Response` with the updated knowledge base and context
- The response can also contain an utterance and a payload that are returned by `handle_text_input`
  or `handle_data_input`
- Finally, the response specifies whether the activity is completed and can contain an optional "choice", depending on
  the type. In a gateway, the choice is the id of the chosen task or `None` to go to the next task if possible. Note
  that the framework does not perform checks on the choice, so it is possible to exit a gateway even if it is not
  completed.

The example below shows a callback that could be associated with an OR, XOR or PARALLEL activity. If the user inserted a
valid choice then the activity is completed, and the callback returns the choice; otherwise it returns an utterance from
the knowledge base.

```Python
from mmcc_framework import Response


def callback(data, kb, context) -> Response:
    # Obtain my_choice from the data, evaluate it and prepare my_payload.
    my_choice = ...
    completed = ...
    my_payload = ...
    ...
    if completed:
        return Response(kb, context, True, payload=my_payload, choice=my_choice)
    return Response(kb, context, False, utterance=kb["my_kb_key"])


def get_callback(activity_id: str):
    """ Given an activity id, this returns the callback corresponding to that activity. """
    return _my_callbacks[activity_id]


_my_callbacks = {
    "my_gateway": callback
    # Add other callbacks here.
}
```

To pass the callbacks to the `Framework`, provide a method that, given the id of the task, returns the correct callback
(without running it), as shown in the example above.

When `handle_text_input` or `handle_data_input` terminate, they return a data structure that contains the utterance and
the payload. The payload contents are not predefined and can be customized.

```Python
{
    "utterance": "An utterance",
    "payload": {...}
}
```

### The knowledge base and the context

These are dictionaries with key-value pairs.

```json
{
  "insert_name": "Please insert your name"
}
```

**SPECIAL KB KEYS:** When a task is starting, the framework **automatically** searches in the knowledge base a value
corresponding to its id and appends its value to the utterance in the `Response`. For example, when a task called
"insert_name" starts, the message in the knowledge base of the example above will be put in the utterance. If you prefer
to handle manually all the utterances, avoid using the id of a task as a knowledge base key.

**SPECIAL CONTEXT KEYS:** In the context, the framework **automatically** adds a `CTX_COMPLETED` key whose value is a
list of task id that can be accessed by the developer in the callbacks: if a gateway (activity with type PARALLEL or OR)
is in this list then it is completed, and the user can move to the next activity. For example when the user has chosen
all the tasks in a PARALLEL activity with the id "my_par", `context[CTX_COMPLETED]` will contain "my_par". The list is
kept clean, meaning that when a gateway is exited, the corresponding entry is removed from the list.

### The NLU adapter

The framework can be used with data (with the method `handle_data_input`) or with text (with `handle_text_input`). The
callbacks expect to receive data as their input, not text. To transform text into data an `NluAdapter` is used. There
are two kinds of adapters: `NoNluAdapter` and `RasaAdapter`

**NoNluAdapter** does not use a NLU engine, and simply takes the input and puts it into a dictionary. The list of keys
to use in the dictionary must be provided to the NoNluAdapter constructor.

```Python
from mmcc_framework import Framework, NoNluAdapter

# Suppose that the framework callbacks use only the following keys: "name" and "occupation".
# Initialize the adapter
my_adapter = NoNluAdapter(["name", "occupation"])
my_framework = Framework(..., nlu=my_adapter)

# Suppose that it is time to insert the name.

# If it is necessary to insert it as text use:
my_framework.handle_text_input("Mark")
# The callback corresponding to the current activity will receive:
data = {"name": "Mark", "occupation": "Mark"}

# If it is necessary to insert the name as data use:
my_framework.handle_data_input({"name": "Mark"})
```

**RasaAdapter** uses [Rasa](https://rasa.com/), to use this adapter it is necessary to first setup and train the
interpreter. The instructions on how to use Rasa are available on Rasa's website, and consist basically in the following
steps:

- Install Rasa and its dependencies;
- Run `rasa init` in your folder of choice;
- Edit the `data/nlu` file with the utterances used for training;
- Run `rasa train nlu` to produce a model;
- Start rasa on port 5005 and pass the location of the model:
  for example `rasa run --enable-api -m models/nlu-20201228-183937.tar.gz`

```Python
from mmcc_framework import Framework, RasaNlu

# Suppose that the nlu is trained with, among the others, the intent "insert_name" with a entity "name".
# Initialize the adapter
my_adapter = RasaNlu()
my_framework = Framework(..., nlu=my_adapter)

# Suppose that it is time to insert the name.

# If it is necessary to insert it as text use:
my_framework.handle_text_input("Mark")
# The callback corresponding to the current activity will receive (if the intent is recognized):
data = {"intent": "insert_name", "name": "Mark"}

# If it is necessary to insert the name as data use:
my_framework.handle_data_input(RasaNlu.dict("insert_name", {"name": "Mark"}))
# This will pass to the callback the same structure as above.
```
