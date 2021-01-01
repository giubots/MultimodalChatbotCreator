# Rasa example

Have a look at the basic example. To use the `RasaNlu` first create a rasa project and train it to obtain a model.
Decompress the model and provide a path to its nlu subdirectory.

This example differs from the basic one only for the structure of the data passed to the callbacks (because the format
of the data depends on the `NluAdapter` used) and the callbacks (because parts of them depend on the data).

Notice how `RasaNlu.dict` method is used to with `handle_data_input` to obtain a uniform data structure, instead of
typing the dictionary by hand.