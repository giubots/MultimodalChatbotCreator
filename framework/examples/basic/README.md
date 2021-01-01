# Basic example

This example shows how to use the framework in an application, without using an NLU engine.

### The process

First the user has to choose whether to write his name or his nickname, then he has to enter his age. The age is
accepted if less than 100 (the threshold is taken from the kb), in the end the data is shown back to the user.

### The interface

This example uses tkinter. The app contains some buttons that can be enabled or not, depending on the current state, and
a chat panel. The chat panel has a large space for the conversation, a one line input field, and a button to send the
text. The text in the field can also be sent pressing return on the keyboard. The chat conversation is shown in the
large text area. The buttons allow to insert a predefined input using data instead of text. Between the buttons and the
chat panel there is a label, the final activity of the process puts here (updating the state through the callbacks) the
final output.

### How it is done

The json files contain the process description and the kb, take some time to inspect them. Notice that the kb contains
some utterances that are not used in the callbacks: the use of default utterances is explained in the framework
documentation.

In the file `my_callbacks.py` there are the callbacks corresponding to each activity specified in the process
description. The following function takes the name of the activity and returns the correct callback, without calling it.

```Python
def get_callback(activity_id: str):
    return _my_callbacks[activity_id]


_my_callbacks = {
    "start": start,
    ...
}
```

The framework is initialized, from the files, with an empty context and a `NoNluAdapter`. When using `from_file`, the
framework takes care of saving the kb back to its file when the process is completed.

```Python
self.framework = Framework.from_file("my_process.json",
                                     "my_kb.json",
                                     {},
                                     get_callback,
                                     NoNluAdapter(["name", "nickname", "age", "name_nickname"]))
```

When the interface receives a textual input , it calls `self.framework.handle_text_input(...)`, the adapter translates
the text input to data input. The data (from the adapter or from `handle_data_input`) is then passed to the callbacks.
The returned utterance is shown to the user, the payload is used to update the state.