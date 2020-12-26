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
        if self._current.type == ActivityType.END:
            return Response({}, {}, True).add_utterance(self._kb, self._current.id).to_dict()

        # If the activity is a XOR, get the choice from the callback.
        if self._current.type == ActivityType.XOR:
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
        if self._current.type == ActivityType.PARALLEL or self._current.type == ActivityType.OR:
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
                    if self._current.type == ActivityType.PARALLEL:
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
                if not a.type == ActivityType.END:
                    raise CallbackException(a.id, "Using the function to get a callback raised an error.") from err
            if not callable(callback):
                raise CallbackException(a.id, "The function to get a callback returned something that is not callable.")


class Response:
    def __init__(self, kb: dict, ctx: dict, complete: bool, utterance: str = None, payload: dict = None,
                 choice: str = None):
        """ Creates a Response with the provided parameters.
        If the current activity is one of ActivityType.get_require_choice(), and is completed, the Response will contain
        the choice of the user. This must be the id of one of the choices provided in the description.

        :param kb: the updated knowledge
        :type kb: dict
        :param ctx: the updated context
        :type ctx: dict
        :param complete: whether the current activity is completed
        :type complete: bool
        :param utterance: an optional utterance to be displayed
        :type utterance: str
        :param payload: an optional payload to be returned to the caller
        :type payload: dict
        :param choice: if the current activity is in ActivityType.get_require_choice() this can contain the user choice
        :type choice: bool
        """
        self.kb = kb
        self.ctx = ctx
        self.complete = complete
        self.utterance = utterance if utterance is not None else ""
        self.payload = payload if payload is not None else {}
        self.choice = choice

    def to_dict(self):
        """ Returns a dictionary with utterance and payload, that can be returned to the caller. """
        return {"utterance": self.utterance, "payload": self.payload}

    def add_utterance(self, kb: dict, key, fallback: str = ""):
        """ Adds an utterance to this response.
        The utterance is taken from the kb using the provided key, if it is not present a fallback (empty by default) is
        used. If this response does not already contain an utterance, in the end it will contain the added utterance.
        If the utterance to add can not be found and a fallback is not provided, nothing is added.
        If an utterance is provided and one already exists, the new one is appended on a new line.

        :param kb: the kb from which to take the utterance to add
        :type kb: dict
        :param key: the key to retrieve the utterance from the kb
        :param fallback: the value that is used if the key is not in the kb
        :type fallback: str
        """
        my_utt = kb[key] if key in kb else fallback
        if self.utterance == "":
            self.utterance = my_utt
        elif my_utt != "":
            self.utterance += "\n" + my_utt
        return self


class Process:
    """ The description of a process, with a list of activities and the id of the first activity.

    :ivar activities: a list of Activity objects representing this process
    :ivar first: the first Activity of the process
    """

    def __init__(self, activities: list, first_activity_id: str):
        """ Creates a new process description with the provided activities and first activity id.

        If the provided activities list contains the activities as dictionaries instead of Activity objects, this will
        call Activity.from_dict(...) on each of them before adding it.

        Example:
            my_process = Process([Activity("one", "two", ActivityType.TASK), ...], "one")

        :param activities: a list of Activity objects or of dictionaries representing the activities of the process
        :type activities: list of Activity or list of dict
        :param first_activity_id: the id of the first Activity of the process (that should have type START)
        :type first_activity_id: str
        :raises DescriptionException: if first activity id has no corresponding activity
        """
        self.activities = []
        for a in activities:
            self.activities.append(a if isinstance(a, Activity) else Activity.from_dict(a))
        try:
            self.first = next(x for x in self.activities if x.id == first_activity_id)
        except StopIteration as err:
            raise DescriptionException(first_activity_id, "Found no activity with the provided id.") from err

    @classmethod
    def from_dict(cls, dictionary):
        """ Given a dictionary representing a Process, this returns the corresponding Process, if possible.

        Example:
            my_process = Process.from_dict({"first_activity_id": "one",
                                            "activities": [{"my_id": "one", "next_id": "two", "my_type": "task"},
                                                           ... ]})


        :return: a Process instance with the provided attributes
        :rtype: Process
        :raises DescriptionException: if the required parameters are not found, or unknown parameters are provided
        """
        try:
            return cls(**dictionary)
        except TypeError as err:
            raise DescriptionException(dictionary, "Did not find a required parameter in the process.") from err

    def _check(self):  # TODO(giulio): check if next == None happens only in a gateway?
        """ Performs some checks on the description, both syntactic and semantic (for example id are unique...).

        :raises DescriptionException: if the check is not passed
        """

        # Assume the first activity id is not found.
        found_first = 0

        for a in self.activities:
            # Check that next id is note equal to id.
            if a.next_id == a.id:
                raise DescriptionException(a.id, "Found an activity that is the next of itself.")

            # Count how many activities have first id as their id.
            if self.first.id == a.id:
                found_first += 1

            # If this is a OR, XOR or PARALLEL, check that choices exist unique.
            choices = {}
            if a.type in ActivityType.get_require_choice():
                # Choices list is provided because of previous checks in Activity constructor.
                for c in a.choices:
                    if c is None:
                        raise DescriptionException(a.id, "Fond an activity that contains None in the choices.")
                    if c == a.id:
                        raise DescriptionException(a.id, "Found an activity with itself in its choices.")
                    if c in choices:
                        raise DescriptionException(a.id, "Found an activity that contains duplicate choices.")
                    choices[c] = 0

            # Also count how many other activities have this next id as their id.
            found_next = 0
            for b in self.activities:
                if b.id == a.next_id:
                    found_next += 1

                # And count how many activities correspond to a choice.
                if b.id in choices:
                    choices[b.id] += 1

            # Raise an exception if a choice does not have a corresponding activity or has more than one.
            for c, v in choices.items():
                if v == 0:
                    raise DescriptionException(a.id, f"The following does not have a corresponding activity: {c}.")
                if v > 1:
                    raise DescriptionException(a.id, f"The following have multiple corresponding activities: {c}.")

            # Raise exceptions if next id or first id do not have exactly one corresponding activity.
            if a.next_id is not None:
                if found_next == 0:
                    raise DescriptionException(a.id, "The provided next id does not have a corresponding activity.")
                if found_next > 1:
                    raise DescriptionException(a.next_id, "Found a next id that has multiple corresponding activities.")
        if found_first == 0:
            raise DescriptionException(self.first.id, "First activity id has no corresponding activity.")
        if found_first > 1:
            raise DescriptionException(self.first.id, "First activity id has multiple corresponding activities.")


class Activity:
    """ An element of a Process description, this represent a single step in which the user has to do something.

    :ivar id: the id of this Activity
    :ivar next_id: the id of the Activity that comes after this, when completed (can be None)
    :ivar type: the ActivityType of this Activity
    :ivar choices: a list of id that this activity offers as choices (can be None)
    """

    def __init__(self, my_id: str, next_id, my_type, choices=None):
        """ Creates a new activity with the provided id, next id, type and choices; performs some checks.

        The parameter next_id is None if the activity is the last "inside" one of the ActivityType.get_require_choice
        gateways.

        :param my_id: the id of this Activity (unique)
        :type my_id: str
        :param next_id: the id of the Activity that comes after this, when completed (can be None)
        :type next_id: str or None
        :param my_type: the ActivityType of this Activity or a string representing it (for example "task" or "start")
        :type my_type: ActivityType or str
        :param choices: the ids that this activity offers as choices (only if type is in ActivityType.get_require_choice())
        :type choices: list of str
        :raises DescriptionException: if choices are provided and not needed, or needed and not provided
        :raises KeyError: if can not recognize the ActivityType provided
        """
        self.id = my_id
        self.next_id = next_id
        self.type = my_type if isinstance(my_type, ActivityType) else ActivityType[my_type.upper()]
        if self.type in ActivityType.get_require_choice():
            if choices is None:
                raise DescriptionException(self.id, "Expected some choices, but found none.")
            if not choices:
                raise DescriptionException(self.id, "Expected some choices, but found an empty list.")
        else:
            if choices is not None or choices:
                raise DescriptionException(self.id, "Found unexpected choices.")
        self.choices = choices

    @classmethod
    def from_dict(cls, dictionary: dict):
        """ Given a dictionary representing an Activity, this returns the corresponding Activity, if possible.

        Example:
            my_activity = Activity.from_dict({"my_id": "an id",
                                              "next_id": "another id",
                                              "my_type": "xor",
                                              "choices": ["id", "more id"]})

        See Activity.__init__ for more info.

        :return: an Activity instance with the provided attributes
        :rtype: Activity
        :raises DescriptionException: if the required parameters are not found, or unknown parameters are provided
        """
        try:
            return cls(**dictionary)
        except TypeError as err:
            raise DescriptionException(dictionary, "Did not find a required parameter in this activity.") from err

    def __eq__(self, o: object) -> bool:
        """ Returns true if two activities have the same attributes. """
        return isinstance(o, Activity) and self.id == o.id and self.next_id == o.next_id and self.type == o.type \
               and self.choices == o.choices

    def __ne__(self, o: object) -> bool:
        """ Returns true if __eq__ would return false. """
        return not self == o


class ActivityType(Enum):
    """ The various types of activities in a process. """

    TASK = "task"
    """ Represents an operation to be done to complete the process.
    The Response contains true if the user can move on to the next activity.
    """
    START = "start"
    """ It is the entry point of the process.
    Its Response must contain True and can be used to prepare the state using the payload.
    """
    END = "end"
    """ A "sink" state, that represents the termination of the process. """
    PARALLEL = "parallel"
    """ A task that gives some options to the user, the user can chose which one to execute.
    This is completed when all options have been chosen at least once.
    Its callback must return the id of the chosen activity if the user input was valid.
    """
    XOR = "xor"
    """ A task that gives some options to the user, the user can chose which one to execute.
    This allows the user to choose exactly one of the options.
    Its callback must return the id of the chosen activity if the user input was valid.
    """
    OR = "or"
    """ A task that gives some options to the user, the user can chose which one to execute.
    This is completed when the user has chosen at least one of the options.
    Its callback must return the id of the chosen activity if the user input was valid.
    """

    @staticmethod
    def get_require_choice():
        """ Returns a list of ActivityType that require some choices to be provided in the description. """
        return [ActivityType.PARALLEL, ActivityType.XOR, ActivityType.OR]


class DescriptionException(Exception):
    """ Exception raised when the check on the process description finds errors or incongruities.

    :ivar cause: the element that caused the error
    :ivar message: the message of this exception
    """

    def __init__(self, cause, message="The process description caused an exception."):
        """ Creates an exception with the provided cause, and an optional message. """
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        """ Presents the message and the cause of this exception. """
        return f"{super().__str__()} The cause of the exception was: {self.cause}"


class CallbackException(Exception):
    """ Exception raised when the check on the callbacks fails.

    :ivar cause: the parameter that caused the exception
    :ivar message: the message of this exception
    """

    def __init__(self, cause, message="A callback caused an exception."):
        """ Creates an exception with the provided cause, and an optional message. """
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        """ Presents the message and the cause of this exception. """
        return f"{super().__str__()} The parameter of the function was: {self.cause}"
