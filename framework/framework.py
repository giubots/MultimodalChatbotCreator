# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo
import json
from collections import deque
from enum import Enum

CTX_COMPLETED = "_done_"
""" Context key whose value is a list of activity id for the pending gateways that allow skipping. """


class Framework:
    # TODO(giulio): fix nlu (token and initialize)
    def __init__(self, process, kb: dict, initial_context: dict, callback_getter, nlu):
        self._process = process if isinstance(process, Process) else Process.from_dict(process)
        self._kb = kb
        self._ctx = initial_context
        self._ctx[CTX_COMPLETED] = []
        self._current = self._process.first
        self.callback_getter = callback_getter
        self._nlu = nlu
        self._stack = deque()
        self._done = {}
        self._check()

    @classmethod
    def from_file(cls, process, kb, initial_context, callback_getter, nlu):
        return cls(json.load(process), json.load(kb), json.load(initial_context), callback_getter, nlu)

    def handle_text_input(self, text):
        return self.handle_data_input(self._nlu(text))

    def handle_data_input(self, data):
        # If the activity is an END, return the default utterance if it exists.
        if self._current.type == Type.END:
            return Response({}, {}, True).add_utterance(self._kb, self._current.id).to_dict()

        # If the activity is a XOR, get the choice from the callback.
        if self._current.type == Type.XOR:
            response = self._get_response(data)

            # If the choice is valid, push next on the stack and continue with the chosen activity.
            if response.complete:
                # Push next id on the stack, can be None.
                self._stack.append(self._current.next_id)

                # Current will not be None, because XOR must return a valid next id.
                self._current = next(x for x in self._process.activities if x.id == response.choice)

                # Add default utterance if it exists.
                response.add_utterance(self._kb, self._current.id)
            return response.to_dict()

        # PARALLEL and OR have similar behaviour and they are handled together.
        if self._current.type == Type.PARALLEL or self._current.type == Type.OR:
            # Obtain the chosen task from the callback.
            response = self._get_response(data)
            if response.complete:
                # The returned task is valid, and can be None to go to the next.
                if response.choice is None:
                    # Clear the info on the current gateway, if some exist.
                    self._done.pop(self._current.id, "")
                    if self._current.id in self._ctx[CTX_COMPLETED]:
                        self._ctx[CTX_COMPLETED].remove(self._current.id)

                    # Go to next task.
                    self._go_next(response)
                else:
                    # Put the gateway on the stack.
                    self._stack.append(self._current.id)

                    # Add an entry for this gateway to done and add the choice to it.
                    if self._current.id not in self._done:
                        self._done[self._current.id] = []
                    if response.choice not in self._done[self._current.id]:
                        self._done[self._current.id].append(response.choice)

                    # Handle separately PARALLEL and OR for updating CTX_COMPLETED.
                    if self._current.type == Type.PARALLEL:
                        # A PARALLEL is completed when all the sub-tasks have been chosen at least once.
                        if all(i in self._done[self._current.id] for i in self._current.choices):
                            # Completed: add to the list.
                            if self._current.id not in self._ctx[CTX_COMPLETED]:
                                self._ctx[CTX_COMPLETED].append(self._current.id)
                        else:
                            # Not completed: remove from the list.
                            if self._current.id in self._ctx[CTX_COMPLETED]:
                                self._ctx[CTX_COMPLETED].remove(self._current.id)
                    else:
                        # An OR is completed after the first valid choice.
                        if self._current.id not in self._ctx[CTX_COMPLETED]:
                            self._ctx[CTX_COMPLETED].append(self._current.id)

                    # Set the choice and optional default utterance, the choice can not be None.
                    self._current = next(x for x in self._process.activities if x.id == response.choice)
                    response.add_utterance(self._kb, self._current.id)
            return response.to_dict()

        # If the activity is TASK or START, the evaluate callback is called.
        response = self._get_response(data)

        # If the activity is completed go to the next.
        if response.complete:
            self._go_next(response)
        return response.to_dict()

    def _get_response(self, data):
        # Run the callback, update the context and the kb, and return the response.
        response = self.callback_getter(self._current.id)(data, self._kb, self._ctx)
        self._kb = response.kb  # TODO(giulio): save kb and check choice
        self._ctx = response.ctx
        return response

    def _go_next(self, response):
        # Go to the next task (maybe from the stack) and add the default utterance if it exists.
        if self._current.next_id is None:
            popped = self._stack.pop()
            while popped is None:
                popped = self._stack.pop()
            self._current = next(x for x in self._process.activities if x.id == popped)
        else:
            self._current = next(x for x in self._process.activities if x.id == self._current.next_id)
        response.add_utterance(self._kb, self._current.id)

    def _check(self):
        """ Checks that all the activities have a callback"""

        callback = ""
        for a in self._process.activities:
            try:
                callback = self.callback_getter(a.id)
            except BaseException as err:
                if not a.type == Type.END:
                    raise CallbackException(a.id, "Using the function to get a callback raised an error.") from err
            if not callable(callback):
                raise CallbackException(a.id, "The function to get a callback returned something that is not callable.")


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
        Process._check(activities, first_activity_id)
        self.activities = []
        for a in activities:
            self.activities.append(a if isinstance(a, Activity) else Activity.from_dict(a))
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
        """ Performs some checks on the description, both syntactic and semantic (for example id are unique...). """

        # Assume the first activity id is not found.
        found_f = 0
        a = ""
        a_id = ""

        try:
            for a in activities:
                a_id = a.id if isinstance(a, Activity) else a["my_id"]

                # Count how many activities have first id as their id.
                if first_activity_id == a_id:
                    found_f += 1

                # Check that the type is valid.
                a_type = a.type if isinstance(a, Activity) else a["my_type"]
                if not isinstance(a_type, Type):
                    try:
                        a_type = Type[a_type]
                    except KeyError:
                        raise DescriptionException(a_id, f"Wrong type: {a_type}.")

                # If this is a OR, XOR or PARALLEL, check that choices are provided (add to list and later cross out).
                choices = []
                if a_type == Type.XOR or a_type == Type.OR or a_type == Type.PARALLEL:
                    choices = (a.choices if isinstance(a, Activity) else a["choices"]).copy()
                    if not choices:
                        raise DescriptionException(a_id, "Found a gateway that does not provide choices.")

                # Also count how many other activities have this next id as their id.
                id_check = a.next_id if isinstance(a, Activity) else a["next_id"]
                if id_check is None:
                    continue
                found_n = 0
                for b in activities:
                    b_id = (b.id if isinstance(b, Activity) else b["my_id"])
                    if id_check == b_id:
                        found_n += 1
                    if b_id in choices:
                        choices.remove(b_id)

                # Raise an exception if a choice does not have a corresponding activity.
                if choices:
                    raise DescriptionException(a_id, f"The following do not have a corresponding activity: {choices}.")

                # Raise exceptions if next id or first id do not have exactly one corresponding activity.
                if found_n == 0:
                    raise DescriptionException(a_id, "The provided next id does not have a corresponding activity.")
                if found_n > 1:
                    raise DescriptionException(id_check, "Found a next id that has multiple corresponding activities.")
            if found_f == 0:
                raise DescriptionException(first_activity_id, "First activity id has no corresponding activity.")
            if found_f > 1:
                raise DescriptionException(first_activity_id,
                                           "First activity id has multiple corresponding activities.")
        except KeyError as error:
            if error.args[0] == "my_id":
                raise DescriptionException(a, "Missing my_id key") from error
            raise DescriptionException(a_id, f'Activity has missing key: {error}.') from error


class Activity:
    """
    An element of a Process description, this represent a single step in which the user has to do something.

    :ivar id: the id of this Activity.
    :ivar next_id: the id of the Activity that comes after this, when completed (can be null).
    :ivar type: the Type of this Activity.
    :ivar choices: a list of id that this activity offers as choices (only for PARALLEL, OR, XOR).
    """

    def __init__(self, my_id: str, next_id: str, my_type, choices=None):
        """
        Creates a new activity with the provided id, next id and type.

        :param my_id: the id of this Activity.
        :param next_id: the id of the Activity that comes after this, when completed (can be null).
        :param my_type: the Type of this Activity or a string representing it (for example "task" or "start").
        :param choices: a list of id that this activity offers as choices (only for PARALLEL, OR, XOR).
        """
        self.id = my_id
        self.next_id = next_id
        self.type = my_type if isinstance(my_type, Type) else Type[my_type.upper()]
        self.choices = choices

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
    Exception raised when the check on the process description finds errors or incongruities.

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


class CallbackException(Exception):
    """
    Exception raised when the check on the callbacks fails.

    :ivar cause: the parameter that caused the exception.
    :ivar message: the message of this exception.
    """

    def __init__(self, cause, message="A callback caused an exception."):
        """ Creates an exception with the provided cause, and an optional message. """
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        """ Presents the message and the cause of this exception. """
        return f"{super().__str__()} The parameter of the function was: {self.cause}"
