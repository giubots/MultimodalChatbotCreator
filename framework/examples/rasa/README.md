# Rasa example

Have a look at the basic example first. To use the `RasaNlu` first create a rasa project and train it to obtain a model.
Start the trained model on port 5005 and pass the model location; to run this example first execute:
`rasa run --enable-api -m rasa_model/nlu-20201228-183937.tar.gz`

This example differs from the basic one only for the structure of the data passed to the callbacks (because the format
of the data depends on the `NluAdapter` used) and for the callbacks (because parts of them depend on the data).

Notice how `RasaNlu.dict` method is used with `handle_data_input` to obtain a uniform data structure, instead of typing
the dictionary by hand.

In `rasa_model/nlu.yml` you can find an example on how the model for this example was trained (using `rasa train nlu`).