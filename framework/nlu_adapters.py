# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo
from abc import ABC, abstractmethod
from typing import Text, Dict, Any

from rasa.nlu.model import Interpreter


class NluAdapter(ABC):
    @abstractmethod
    def parse(self, utterance: Text) -> Dict[Text, Any]:
        raise NotImplementedError()


class RasaNluAdapter(NluAdapter):

    def __init__(self, path: Text) -> None:
        self.interpreter = Interpreter.load(model_dir=path)

    def parse(self, utterance: Text) -> Dict[Text, Any]:
        return self.interpreter.parse(text=utterance)
