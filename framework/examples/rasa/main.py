# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo

from examples.rasa.my_callbacks import get_callback
from mccreator_framework.framework import *

# A nlu implementation that takes the text input and puts it into a dict.
# This is needed to abstract the nlu dependency in this first phase of the project implementation.
from mccreator_framework.nlu_adapters import RasaNlu


# A helper function that extracts the information from the payload of the response and returns an updated state.
def get_state(response):
    return {
        "BA": "BA" in response["payload"] and response["payload"]["BA"],
        "BB": "BB" in response["payload"] and response["payload"]["BB"],
        "BC": "BC" in response["payload"] and response["payload"]["BC"],
        "BD": "BD" in response["payload"] and response["payload"]["BD"],
        "FC": "FC" in response["payload"] and response["payload"]["FC"],
        "FC_c": response["payload"]["FC_c"] if "FC_c" in response["payload"] else "empty"
    }


def on_save(kb: dict, kb_file):
    kb_file.seek(0)
    json.dump(kb, kb_file, indent=2)
    kb_file.truncate()
    kb_file.close()


# Example of how the framework can be used.
# Let's suppose that the user has a chat panel, some buttons that can be hidden, and a field that will
# contain the data he has inserted. The user has to insert his name XOR nickname, then his age, and then he will see
# both his name and age in the field FC.
# He can insert the data in the chat panel, or if he presses BA he will insert a default name, "Bob",
# if he presses the button BB he will insert a default age, 50.
# The operations must be performed in the correct order, also if performed via GUI.
# The framework will interact with the GUI via the data structure returned by the handle_input method.
# The developer writes a knowledge base, in this case it contains the utterances that are shown to the user when an
# activities starts, some other utterances, and a constraint on the age.
if __name__ == '__main__':
    # The initial context is empty, instead of the token, here a callback is forwarded to the framework.
    # The developer creates a framework (which is immediately initialized)
    my_kb = open("my_kb.json", "r+")
    with open("my_process.json") as my_process, open("my_context.json") as my_ctx:
        my_framework = Framework(json.load(my_process),
                                 json.load(my_kb),
                                 json.load(my_ctx),
                                 get_callback,
                                 RasaNlu("rasa_project\\models\\nlu-20201228-183937\\nlu"),
                                 lambda kb: on_save(kb, my_kb))

    # The application takes the input from the keyboard and forwards it to the framework, the response is printed out.
    # To quickly simulate a GUI interaction, the application prints BA, BB, FC if the respective elements are visible,
    # and the input "BA" is managed as if the user interacted with BA.
    # The user should insert "BA" only if BA is visible, otherwise the behaviour is not correct.
    # To close the program, the user has to type "quit".
    u_in = ""
    while u_in != "quit":
        # handle input and update the state
        if u_in == "BA":
            my_response = my_framework.handle_data_input(RasaNlu.dict("choose_name_nickname", {"name": "Bob"}))
        elif u_in == "BB":
            my_response = my_framework.handle_data_input(RasaNlu.dict("choose_age", {"age": "50"}))
        elif u_in == "BC":
            my_response = my_framework.handle_data_input(RasaNlu.dict("choose_name"))
        elif u_in == "BD":
            my_response = my_framework.handle_data_input(RasaNlu.dict("choose_nickname"))
        else:
            my_response = my_framework.handle_text_input(u_in)
        state = get_state(my_response)

        # print the "GUI"
        if state["BA"]:
            print("BA - Insert Bob")
        if state["BB"]:
            print("BB - Insert 50")
        if state["BC"]:
            print("BC - Choose to insert name")
        if state["BD"]:
            print("BD - Choose to insert nickname")
        if state["FC"]:
            print("FC:", state["FC_c"])

        # print the "chat panel"
        if "utterance" in my_response:
            print("chat:", my_response["utterance"])

        # take next input
        u_in = input()
