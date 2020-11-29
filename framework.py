# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo


class Framework:
    # TODO(giulio): fix nlu (token and initialize); maybe put the description in classes and check it is correct
    def __init__(self, process, kb, initial_context, nlu):
        self._process = process
        self._kb = kb
        self._ctx = initial_context
        self._currentId = process["first_activity_id"]
        self._nlu = nlu

    def handle_text_input(self, text):
        return self.handle_data_input(self._nlu(text))

    def handle_data_input(self, data):
        current = next(x for x in self._process["activities"] if x["id"] == self._currentId)

        # If the activity is an END, then it returns the initial utterance if exists.
        if current["type"] == "END":
            return {"utt": self._kb[current["id"]] if current["id"] in self._kb else ""}

        # If the activity is TASK or START, the evaluate callback is called and the data is updated.
        self._kb, self._ctx, response, completed = current["evaluate"](data, self._kb, self._ctx)

        # If the activity is completed, update the current id and add the next initial utterance to the response
        if completed:
            self._currentId = current["next_id"]
            if current["next_id"] in self._kb:
                if "utt" in response:
                    response["utt"] = response["utt"] + "\n" + self._kb[current["next_id"]]
                else:
                    response["utt"] = self._kb[current["next_id"]]

        return response
