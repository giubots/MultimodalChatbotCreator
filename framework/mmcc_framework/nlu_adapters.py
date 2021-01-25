import json
from abc import ABC, abstractmethod
from http.client import HTTPConnection
from typing import Dict, Any, List


class NluAdapter(ABC):
    """ A class that provides a method to transform the text input into the equivalent data input."""

    @abstractmethod
    def parse(self, utterance: str) -> Dict[str, Any]:
        """ Transforms the provided text input into the equivalent data input. """
        raise NotImplementedError()


class NoNluAdapter(NluAdapter):
    """ This adapter does not use a NLU engine, and simply takes the input and puts it into a dictionary.

    The list of keys to use in the dictionary must be provided to the NoNluAdapter constructor.

    Example:
        Suppose that the framework callbacks use only the following keys: "name" and "occupation".
        Initialize the adapter: `my_adapter = NoNluAdapter(["name", "occupation"])`.

        Suppose that it is time to insert the name. If it is necessary to insert it as text use:
        `my_framework.handle_text_input("Mark")`. The callback corresponding to the current activity will receive:
        `{"name": "Mark", "occupation": "Mark"}`.

        If it is necessary to insert the name as data use: `my_framework.handle_data_input({"name": "Mark"})`.

    :ivar keys: the list of keys that are used in the callbacks
    """

    def __init__(self, expected_keys: List[str]) -> None:
        """ Initializes this adapter with the provided list of keys.

        :param expected_keys: the list of keys that are used in the callbacks
        """
        self.keys = expected_keys.copy()

    def parse(self, utterance: str) -> Dict[str, Any]:
        """ Provides a dictionary containing the utterance as the value for each key in self.keys.

        :param utterance: the text input from the user
        :return: a dictionary containing the utterance as the value for each key in self.keys
        """
        return dict.fromkeys(self.keys, utterance)


class RasaNlu(NluAdapter):
    """ This adapter uses Rasa, to use this adapter it is necessary to first setup and train the interpreter.

    The instructions on how to use Rasa are available on Rasa's website, and consist basically in the following steps:

    - Install Rasa and its dependencies;
    - Run `rasa init` in your folder of choice;
    - Edit the `data/nlu` file with the utterances used for training;
    - Run `rasa train nlu` to produce a model;
    - Start rasa on port 5005 and pass the location of the model:
      for example `rasa run --enable-api -m models/nlu-20201228-183937.tar.gz`

    Example:
        Suppose that the nlu is trained with, among the others, the intent "insert_name" with a entity "name".
        Initialize the adapter: `my_adapter = RasaNlu()`

        Suppose that it is time to insert the name. If it is necessary to insert it as text use:
        `my_framework.handle_text_input("Mark")`. The callback corresponding to the current activity will receive
        (if the intent is recognized): `{"intent": "insert_name", "name": "Mark"}`.

        If it is necessary to insert the name as data use:
        `my_framework.handle_data_input(RasaNlu.dict("insert_name", {"name": "Mark"}))`, which will pass to the callback
        the same structure as above.

    :ivar interpreter: the instance of the rasa interpreter used by this adapter
    """

    def parse(self, utterance: str) -> Dict[str, Any]:
        """ Runs the interpreter to parse the given utterance and returns a dictionary containing the parsed data.

        If no intent can be extracted from the provided utterance, this returns an empty dictionary.

        :param utterance: the text input from the user
        :return: a dictionary containing the detected intent and corresponding entities if any exists.
        """
        connection = HTTPConnection("localhost:5005") # TODO modify here to use without docker
        connection.request("POST", "/model/parse", json.dumps({"text": utterance}))
        response = json.loads(connection.getresponse().read())
        if response["intent"]["name"] is None:
            return {"intent": ""}
        return self.dict(response["intent"]["name"],
                         {item['entity']: item["value"] for item in response["entities"]})

    @staticmethod
    def dict(intent: str, values: Dict[str, Any] = None) -> Dict[str, Any]:
        """ Helper method that can be used to produce a dictionary equivalent to the one of the parse method.
        Use this method with framework.handle_data_input.

        :param intent: the intent corresponding to this input
        :param values: an optional dictionary containing pairs of entity-value
        :return: a dictionary equivalent to the one produced by the parse method
        """
        if values is None:
            values = {}
        return {"intent": intent, **values}
