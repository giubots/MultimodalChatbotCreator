# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo
from abc import ABC, abstractmethod
from typing import Text, Dict, Any, List


class NluAdapter(ABC):
    @abstractmethod
    def parse(self, utterance: Text) -> Dict[Text, Any]:
        raise NotImplementedError()


class NoNluAdapter(NluAdapter):
    def __init__(self, expected_keys: List) -> None:
        self.keys = expected_keys.copy()

    def parse(self, utterance: Text) -> Dict[Text, Any]:
        return dict.fromkeys(self.keys, utterance)


# TODO(giulio): investigate if this can support multiple frameworks
# TODO(giulio): fix import
class RasaNlu(NluAdapter):

    def __init__(self, path: Text) -> None:
        from rasa.nlu.model import Interpreter
        self.interpreter = Interpreter.load(model_dir=path)

    def parse(self, utterance: Text) -> Dict[Text, Any]:
        response = self.interpreter.parse(text=utterance)
        if response["intent"]["name"] is None:
            return {}
        return self.dict(response["intent"]["name"],
                         {item['entity']: item["value"] for item in response["entities"]})

    @staticmethod
    def dict(intent: Text, values: Dict[Text, Any] = None):
        if values is None:
            values = {}
        return {"intent": intent, **values}
