from abc import ABC, abstractmethod
from typing import Dict, Any, List


class NluAdapter(ABC):
    """ A class that provides a method to transform the text input into the equivalent data input."""

    @abstractmethod
    def parse(self, utterance: str) -> Dict[str, Any]:
        """ Transforms the provided text input into the equivalent data input. """
        raise NotImplementedError()


class NoNluAdapter(NluAdapter):
    """ This adapter does not use a NLU engine, and simply takes the input and puts it into a dictionary.

    Example:
        Suppose that the framework callbacks use only the following keys: "name" and "occupation".
        Suppose that it is time to insert the name.

        If it is necessary to insert it as text, my_framework.handle_text_input("Mark") will call the callback
        corresponding to the current activity passing as data:

        {"name": "Mark", "occupation": "Mark"}

        The method my_framework.handle_data_input should be called, for example, with {"name": "Mark"}.

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
    """ This adapter uses RASA, to use this adapter it is necessary to first setup and train the interpreter.

    The instructions to use rasa are available on rasa's website, and consists basically in the following steps:
    * Install rasa and its dependencies;
    * Run rasa init in your folder of choice;
    * Edit the data/nlu file with the utterances used for training;
    * Run rasa train nlu to produce a model.
    Then it is necessary to decompress the model folder, this will contain a "nlu" subdirectory.

    Example:
        Suppose that the nlu is trained with, among the others, the intent "insert_name" with a entity "name".
        Suppose that it is time to insert the name.

        If it is necessary to insert it as text, my_framework.handle_text_input("Mark") will call the callback
        corresponding to the current activity passing as data, if the intent is correctly recognized:

        {"intent": "insert_name", "name": "Mark"}

        The method my_framework.handle_data_input should be called, for example, with RasaNlu.dict("insert_name",
        {"name": "Mark"}), which will pass to the callback the same structure above.

    :ivar interpreter: the instance of the rasa interpreter used by this adapter
    """

    def __init__(self, path: str) -> None:
        """ Initializes this adapter with an interpreter from a rasa project.

        :param path: path of the (decompressed) model "nlu" subdirectory, for example "PathToMyModel/nlu"
        """
        from rasa.nlu.model import Interpreter
        self.interpreter = Interpreter.load(model_dir=path)

    def parse(self, utterance: str) -> Dict[str, Any]:
        """ Runs the interpreter to parse the given utterance and returns a dictionary containing the parsed data.

        If no intent can be extracted from the provided utterance, this returns an empty dictionary.

        :param utterance: the text input from the user
        :return: a dictionary containing the detected intent and corresponding entities if any exists.
        """
        response = self.interpreter.parse(text=utterance)
        if response["intent"]["name"] is None:
            return {}
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
