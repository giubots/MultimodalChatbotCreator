# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo
import json
from collections import deque
from enum import Enum


class Framework:
    # TODO(giulio): fix nlu (token and initialize)
    def __init__(self, process, kb: dict, initial_context: dict, callback_getter, nlu):
        self._process = process if isinstance(process, Process) else Process.from_dict(process)
        self._kb = kb
        self._ctx = initial_context
        self._current = self._process.first
        self.callback_getter = callback_getter
        self._nlu = nlu
        self._stack = deque()

    @classmethod
    def from_file(cls, process, kb, initial_context, callback_getter, nlu):
        return cls(json.load(process), json.load(kb), json.load(initial_context), callback_getter, nlu)

    def handle_text_input(self, text):
        return self.handle_data_input(self._nlu(text))

    def handle_data_input(self, data):
        # If the activity is an END, then it returns the default utterance if it exists.
        if self._current.type == Type.END:
            return Response({}, {}, True).add_utterance(self._kb, self._current.id).to_dict()

        # If the activity is a XOR, get the choice from the callback.
        # If the choice is valid, push next on the stack and continue with the chosen activity.
        if self._current.type == Type.XOR:
            response = self.callback_getter(self._current.id)(data, self._kb, self._ctx)
            self._kb = response.kb
            self._ctx = response.ctx
            if response.complete:
                self._stack.append(self._current.next_id)
                self._current = next(x for x in self._process.activities if x.id == response.choice)
                response.add_utterance(self._kb, self._current.id)
            return response.to_dict()

        # If the activity is TASK or START, the evaluate callback is called and the data is updated.
        response = self.callback_getter(self._current.id)(data, self._kb, self._ctx)
        self._kb = response.kb
        self._ctx = response.ctx

        # If the activity is completed, update current and add the next default utterance to the response
        # If the next activity is None, try to pop one from the stack.
        if response.complete:
            if self._current.next_id is None:
                popped = self._stack.pop()
                while popped is None:
                    popped = self._stack.pop()
                self._current = next(x for x in self._process.activities if x.id == popped)
            else:
                self._current = next(x for x in self._process.activities if x.id == self._current.next_id)
            response.add_utterance(self._kb, self._current.id)
        return response.to_dict()


class Response:
    def __init__(self, kb: dict, ctx: dict, complete: bool, utterance="", payload=None, choice=""):
        self.kb = kb
        self.ctx = ctx
        self.complete = complete
        self.utterance = utterance
        self.payload = payload if payload is not None else {}
        self.choice = choice

    def to_dict(self):
        return {"utt": self.utterance, "payload": self.payload}

    def add_utterance(self, kb: dict, key, fallback=""):
        """
        Returns a dictionary with a "utt" key.

        The value of "utt" is taken from from kb[key] if it exists, else a fallback is used. If a response is provided,
        the utterance is added to it and the other contents are not modified. If the provided response already contains
        a "utt" element, and the value to add is not empty, the new value is appended to the one provided, on a new line.

        :param kb: a dictionary that can contain the value to add.
        :param key: the key to access the value to add.
        :param fallback: if kb does not contain the key, then this fallback is used.
        :param response: an existing response to which the new value is added.
        :return: a dictionary with an "utt" key.
        """  # TODO
        my_utt = kb[key] if key in kb else fallback
        if self.utterance == "":
            self.utterance = my_utt
        elif my_utt != "":
            self.utterance += "\n" + my_utt
        return self


class Process:
    """
    The description of a process, with a list of activities and the id of the first activity.

    :ivar activities: a list of Activity objects representing this process.
    :ivar first: the first Activity of the process.
    """

    def __init__(self, activities: list, first_activity_id: str):
        """
        Creates a new process description with the provided activities and first activity id.

        If the provided activities list contains the activities as dictionaries instead of Activity objects, this will
        call Activity.from_dict(...) on each of them before adding it.
        Before returning, this checks that the process is sound.

        :param activities: a list of Activity objects or of dictionaries representing the activities.
        :param first_activity_id: the id of the first Activity of the process.
        """
        self.activities = []
        for a in activities:
            self.activities.append(a if isinstance(a, Activity) else Activity.from_dict(a))
        Process._check(activities, first_activity_id)
        self.first = next(x for x in self.activities if x.id == first_activity_id)

    @classmethod
    def from_dict(cls, dictionary):
        """ Given a dictionary representing a Process, this returns the corresponding Process, if possible. """
        return cls(**dictionary)

    @classmethod
    def from_file(cls, fp):
        """
        Given a file containing a dictionary or json description, this returns the corresponding Process, if possible.

        Example:
            myProcess = Process.from_file(open("my_process.json"))
        """
        return cls.from_dict(json.load(fp))

    @staticmethod
    def _check(activities: list, first_activity_id: str):
        """ Checks that all the id exist and are unique. """

        # Assume the first activity id is not found
        found_f = 0

        # Count how many activities have first id as their id
        for a in activities:
            if first_activity_id == (a.id if isinstance(a, Activity) else a["my_id"]):
                found_f += 1

            # Also count how many other activities have this next id as their id
            id_check = a.next_id if isinstance(a, Activity) else a["next_id"]
            if id_check is None:
                continue
            found_n = 0
            for b in activities:
                if id_check == (b.id if isinstance(b, Activity) else b["my_id"]):
                    found_n += 1

            # Raise exceptions if next id or first id do not have exactly one corresponding activity
            if found_n == 0:
                raise DescriptionException(id_check, "Found a next id that has no corresponding activity.")
            if found_n > 1:
                raise DescriptionException(id_check, "Found a next id that has multiple corresponding activities.")
        if found_f == 0:
            raise DescriptionException(first_activity_id, "First activity id has no corresponding activity.")
        if found_f > 1:
            raise DescriptionException(first_activity_id, "First activity id has multiple corresponding activities.")


class Activity:
    """
    An element of a Process description, this represent a single step in which the user has to do something.

    :ivar id: the id of this Activity.
    :ivar next_id: the id of the Activity that comes after this, when completed (can be null).
    :ivar type: the Type of this Activity.
    """

    def __init__(self, my_id: str, next_id: str, my_type):
        """
        Creates a new activity with the provided id, next id and type.

        :param my_id: the id of this Activity.
        :param next_id: the id of the Activity that comes after this, when completed (can be null).
        :param my_type: the Type of this Activity or a string representing it (for example "task" or "start").
        """
        self.id = my_id
        self.next_id = next_id
        self.type = my_type if isinstance(my_type, Type) else Type[my_type.upper()]

    @classmethod
    def from_dict(cls, dictionary):
        """ Given a dictionary representing an Activity, this returns the corresponding Activity, if possible. """
        return cls(**dictionary)


class Type(Enum):
    """ The various types of activities in a process. More info in the README file. """

    TASK = "task"
    START = "start"
    END = "end"
    PARALLEL = "parallel"
    XOR = "xor"
    OR = "or"


class DescriptionException(Exception):
    """
    Exception raised when the check on the process description finds incongruities.

    :ivar cause: the element that caused the error.
    :ivar message: the message of this exception.
    """

    def __init__(self, cause, message="The process description caused an exception."):
        """ Creates an exception with the provided cause, and an optional message. """
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        """ Presents the message and the cause of this exception. """
        return f"{super().__str__()} The cause of the exception was: {self.cause}"
