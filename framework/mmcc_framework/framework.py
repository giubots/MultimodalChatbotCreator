import collections
import json
from collections import deque
from enum import Enum
from threading import Lock
from typing import Union, Optional, List, Dict, Any, Callable

from mmcc_framework.nlu_adapters import NluAdapter

CTX_COMPLETED = "_done_"
""" Context key whose value is a list of activity id for the pending gateways that allow skipping. """


class Framework(object):
    """ A sort of state machine, takes a process description and handles inputs, keeping track of the current activity.

    :ivar _process: an object that represents the process for this Framework instance
    :ivar _kb: the data that is saved between different process executions
    :ivar _ctx: the data that is not saved between different process executions
    :ivar _current: the activity of the process that is being executed
    :ivar _callback_getter: a function that returns the callback of an activity given its id
    :ivar _nlu: provides a translation from text to data, to handle in the same way text and data input (multimodal)
    :ivar _on_save: a function called when it is time to save the kb
    :ivar _stack: a pile of Activity id that is used to handle the gateways
    :ivar _done: a list that is used to determine if a gateway is completed
    """

    def __init__(self,
                 process: Union["Process", Dict[str, Any], Callable[[], Union["Process", Dict[str, Any]]]],
                 kb: Union[Dict[str, Any], Callable[[], Dict[str, Any]]],
                 initial_context: Dict[str, Any],
                 callback_getter: Callable[
                     [str], Callable[[Dict[str, Any], Dict[str, Any], Dict[str, Any]], "Response"]],
                 nlu: NluAdapter,
                 on_save: Callable[[Dict[str, Any]], None]) -> None:
        """ Instantiates a Framework with the given parameters, then performs a check.

        The process parameter can be a Process instance or a dictionary representing a process. In alternative, it can
        also be a function that returns a Process or a dictionary.
        Similarly, the kb parameter can be a dictionary or a callback that returns a dictionary.

        :param process: the Process for this instance, a dictionary representing it, or a callable that provides it
        :param kb: the data that is saved between different process executions
        :param initial_context: can be empty or contain configuration variables
        :param callback_getter: a function that returns the callback of an activity given its id
        :param nlu: provides a translation from text to data, to handle in the same way text and data input
        :param on_save: the function called when it is time to save the kb
        """
        if callable(process):
            process = process()
        self._process = process if isinstance(process, Process) else Process.from_dict(process)
        if callable(kb):
            kb = kb()
        self._kb = kb
        self._ctx = initial_context
        self._ctx[CTX_COMPLETED] = []
        self._current = self._process.first
        self._callback_getter = callback_getter
        self._nlu = nlu
        self._on_save = on_save
        self._stack = deque()
        self._done = {}
        self._check()

    @classmethod
    def from_file(cls,
                  process: str,
                  kb: str,
                  initial_context: Union[str, Dict[str, Any]],
                  callback_getter: Callable[
                      [str], Callable[[Dict[str, Any], Dict[str, Any], Dict[str, Any]], "Response"]],
                  nlu: NluAdapter,
                  lock: Lock = Lock()) -> "Framework":
        """ Loads the configuration of a framework from the files provided.

        The process file must contain a Process description that will be handled by Process.fromDict().
        The kb and context files must contain a dictionary, the context can also be provided directly.
        The kb will be saved back to its file when the process is completed.
        If exists the possibility that the files will be handled by more than one Framework instance at the time, it is
        necessary to provide a unique lock shared by all the instances. This will allow the framework to correctly
        handle the concurrency.

        :param process: the path to a file containing the process description
        :param kb: the path to a file containing the kb
        :param initial_context: the context or the path to a file containing the context
        :param callback_getter: a function that returns the callback of an activity given its id
        :param nlu: provides a translation from text to data, to handle in the same way text and data input
        :param lock: a unique lock shared by all the instances that can use the files
        """
        with lock:
            if not isinstance(initial_context, dict):
                with open(initial_context) as ctx_file:
                    my_ctx = json.load(ctx_file)
            else:
                my_ctx = initial_context

            with open(process) as process_file, open(kb) as kb_file:
                my_framework = cls(json.load(process_file),
                                   json.load(kb_file),
                                   my_ctx,
                                   callback_getter,
                                   nlu,
                                   lambda kb_c: _on_file_save(kb_c, kb, lock))
        return my_framework

    def handle_text_input(self, text: str) -> Dict[str, Any]:
        """ Takes textual input from the user, uses the nlu to parse it, and handles the input as data.

        :param text: the textual input from the user, to be parsed
        :return: a dictionary containing an utterance and a payload
        """
        return self.handle_data_input(self._nlu.parse(text.rstrip()))

    def handle_data_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """ Takes data input from the user and handles it.

        This will call the current activity callback and pass to it the data, then will forward the returned response
        utterance and payload to the caller.
        If the callback signals that the activity was completed successfully, this moves to the next activity in the
        process.

        :param data: the data representing the input from the user, formatted accordingly to the chosen NluAdapter
        :return: a dictionary containing an utterance and a payload
        """
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

                # If the task is END, save the KB.
                if self._current.type == ActivityType.END:
                    self._on_save(self._kb)
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

                    # If the task is END, save the KB.
                    if self._current.type == ActivityType.END:
                        self._on_save(self._kb)
            return response.to_dict()

        # If the activity is TASK or START, the evaluate callback is called.
        response = self._get_response(data)

        # If the activity is completed go to the next.
        if response.complete:
            self._go_next(response)
        return response.to_dict()

    def _get_response(self, data):
        # Run the callback, update the context and the kb, and return the response.
        response = self._callback_getter(self._current.id)(data, self._kb, self._ctx)
        self._kb = response.kb
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

        # If the task is END, save the KB.
        if self._current.type == ActivityType.END:
            self._on_save(self._kb)

    def _check(self):
        """ Checks that all the activities have a callback. """
        callback = ""
        for a in self._process.activities:
            try:
                callback = self._callback_getter(a.id)
            except BaseException as err:
                if not a.type == ActivityType.END:
                    raise CallbackException(a.id, "Using the function to get a callback raised an error.") from err
            if not callable(callback):
                raise CallbackException(a.id, "The function to get a callback returned something that is not callable.")


def _on_file_save(contents: Dict[str, Any], path: str, lock: Lock) -> None:
    """ The callback used to save a json formatted dictionary to a file.

    If the file is shared, provide a lock that is unique for all the instances, and this method will handle concurrent
    access to the file.

    :param contents: the dictionary to save
    :param path: the path of the destination file
    :param lock: a lock shared by all instances that have access to the file
    """
    with lock:
        with open(path, "w") as kb_file:
            json.dump(contents, kb_file, indent=2)


class Response(object):
    def __init__(self,
                 kb: Dict[str, Any],
                 ctx: Dict[str, Any],
                 complete: bool,
                 utterance: str = None,
                 payload: Dict[str, Any] = None,
                 choice: str = None) -> None:
        """ Creates a Response with the provided parameters.

        If the current activity is one of ActivityType.get_require_choice(), and is completed, the Response will contain
        the choice of the user. This must be the id of one of the choices provided in the description.

        :param kb: the updated knowledge
        :param ctx: the updated context
        :param complete: whether the current activity is completed
        :param utterance: an optional utterance to be displayed
        :param payload: an optional payload to be returned to the caller
        :param choice: if the current activity is in ActivityType.get_require_choice() this can contain the user choice
        """
        self.kb = kb
        self.ctx = ctx
        self.complete = complete
        self.utterance = utterance if utterance is not None else ""
        self.payload = payload if payload is not None else {}
        self.choice = choice

    def to_dict(self) -> Dict[str, Any]:
        """ Returns a dictionary with utterance and payload, that can be returned to the caller. """
        return {"utterance": self.utterance, "payload": self.payload}

    def add_utterance(self, kb: Dict[str, Any], key: str, fallback: str = "") -> "Response":
        """ Adds an utterance to this response.

        The utterance is taken from the kb using the provided key, if it is not present a fallback (empty by default) is
        used. If this response does not already contain an utterance, in the end it will contain the added utterance.
        If the utterance to add can not be found and a fallback is not provided, nothing is added.
        If an utterance is provided and one already exists, the new one is appended on a new line.

        :param kb: the kb from which to take the utterance to add
        :param key: the key to retrieve the utterance from the kb
        :param fallback: the value that is used if the key is not in the kb
        :return: the updated Response
        """
        my_utt = kb[key] if key in kb else fallback
        if self.utterance == "":
            self.utterance = my_utt
        elif my_utt != "":
            self.utterance += "\n" + my_utt
        return self


class Process(object):
    """ The description of a process, with a list of activities and the first activity.

    :ivar activities: a list of Activity objects representing this process
    :ivar first: the first Activity of the process
    """

    def __init__(self, activities: List[Union["Activity", Dict[str, Any]]], first_activity_id: str) -> None:
        """ Creates a new process description with the provided activities and first activity id.

        If the provided activities list contains the activities as dictionaries instead of Activity objects, this will
        call Activity.from_dict(...) on each of them before adding it.

        Example:
            my_process = Process([Activity("one", "two", ActivityType.TASK), ...], "one")

        :param activities: a list of Activity objects or of dictionaries representing the activities of the process
        :param first_activity_id: the id of the first Activity of the process (that should have type START)
        :raises DescriptionException: if first activity id has no corresponding activity
        """
        self.activities = []
        for a in activities:
            self.activities.append(a if isinstance(a, Activity) else Activity.from_dict(a))
        try:
            self.first = next(x for x in self.activities if x.id == first_activity_id)
        except StopIteration as err:
            raise DescriptionException(first_activity_id, "Found no activity with the provided id.") from err
        self._check()

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> "Process":
        """ Given a dictionary representing a Process, this returns the corresponding Process, if possible.

        Example:
            my_process = Process.from_dict({
                            "first_activity_id": "one",
                            "activities": [
                                { "my_id": "one", "next_id": "two", "my_type": "task" },
                                ...
                            ]})


        :param dictionary: a dictionary that represents a Process
        :return: a Process instance with the provided attributes
        :raises DescriptionException: if the required parameters are not found, or unknown parameters are provided
        """
        try:
            return cls(**dictionary)
        except TypeError as err:
            raise DescriptionException(dictionary, "Did not find a required parameter in the process.") from err

    def _check(self) -> None:
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


class Activity(object):
    """ An element of a Process description, this represents a single step in which the user has to do something.

    :ivar id: the id of this Activity
    :ivar next_id: the id of the Activity that comes after this, when completed (can be None)
    :ivar type: the ActivityType of this Activity
    :ivar choices: a list of id that this activity offers as choices (can be None)
    """

    def __init__(self,
                 my_id: str,
                 next_id: Optional[str],
                 my_type: Union[str, "ActivityType"],
                 choices: List[str] = None) -> None:
        """ Creates a new activity with the provided id, next id, type and choices; performs some checks.

        The parameter next_id is None if the activity is the last "inside" one of the ActivityType.get_require_choice()
        gateways.

        :param my_id: the id of this Activity (unique)
        :param next_id: the id of the Activity that comes after this, when completed (can be None)
        :param my_type: the ActivityType of this Activity or a string representing it (for example "task" or "start")
        :param choices: the ids that this activity offers as choices (only if type is ActivityType.get_require_choice())
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
    def from_dict(cls, dictionary: Dict[str, Any]) -> "Activity":
        """ Given a dictionary representing an Activity, this returns the corresponding Activity, if possible.

        Example:
            my_activity = Activity.from_dict({"my_id": "an id",
                                              "next_id": "another id",
                                              "my_type": "xor",
                                              "choices": ["id", "more id"]})

        See Activity.__init__ for more info.

        :param dictionary: a dictionary that represents an Activity
        :return: an Activity instance with the provided attributes
        :raises DescriptionException: if the required parameters are not found, or unknown parameters are provided
        """
        try:
            return cls(**dictionary)
        except TypeError as err:
            raise DescriptionException(dictionary, "Did not find a required parameter in this activity.") from err

    def __eq__(self, o: object) -> bool:
        """ Returns true if two activities have the same attributes. """
        return isinstance(o, Activity) and \
               self.id == o.id and self.next_id == o.next_id and self.type == o.type and self.choices == o.choices

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
    def get_require_choice() -> List["ActivityType"]:
        """ Returns a list of the ActivityType that require some choices to be provided in the description. """
        return [ActivityType.PARALLEL, ActivityType.XOR, ActivityType.OR]


class DescriptionException(Exception):
    """ Exception raised when the check on the process description finds errors or incongruities.

    :ivar cause: the element that caused the error
    :ivar message: the message of this exception
    """

    def __init__(self, cause, message: str = "The process description caused an exception.") -> None:
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

    def __init__(self, cause, message: str = "A callback caused an exception.") -> None:
        """ Creates an exception with the provided cause, and an optional message. """
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        """ Presents the message and the cause of this exception. """
        return f"{super().__str__()} The parameter of the function was: {self.cause}"
