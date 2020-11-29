# (C) Copyright 2020 Giulio Antonio Abbo, Pier Carlo Cadoppi, Davide Savoldelli.
# All rights reserved.
# This file is part of the "Multimodal chatbot creator" project.
#
# Author: Giulio Antonio Abbo


from framework import Framework

# Example of how the framework can be used.
# Let's suppose that the user has a chat panel and two buttons, BA and BB, that can be hidden, and a field FC that will
# contain the data he has inserted. The user has to insert his name, then his age, and then he will see both his name
# and age in the field FC. He can insert the data in the chat panel, or if he presses BA he will insert a default name,
# "Bob", if he presses the button BB he will insert a default age, 50.
# The operations must be performed in the correct order, also if performed via GUI.
# The framework will interact with the GUI via the data structure returned by the handle_input method.
if __name__ == '__main__':
    # A nlu implementation that takes the text input and puts it into a dict.
    # This is needed to abstract the nlu dependency in this first phase of the project implementation.
    def stupid_nlu(text):
        return {"name": text, "age": text}


    # The developer writes the callbacks:
    # evaluate(data: dict, kb: dict, context: dict)->(kb, context, response: dic, completed: bool)
    # data is the data provided with handle_input; the function will update kb and context if necessary, then return
    # them, along with a response and a bool indicating whether the current activity is completed.
    # The response can contain an utterance "utt" and a payload that modifies the GUI, both optional.
    # When a task is completed the framework will append the next task initial utterance to the provided one.
    # The optional initial utterance is taken from the KB, being the element with the activity id as a key.
    def start(data, kb, context):
        return kb, context, {"BA": True, "BB": False, "FC": False, "FC_c": ""}, True


    def insert_name(data, kb, context):
        if "name" in data and data["name"] != "":
            context["name"] = data["name"]
            return kb, context, {"BA": False, "BB": True}, True
        return kb, context, {"utt": kb["insert_name_err"]}, False


    def insert_age(data, kb, context):
        if "age" in data:
            try:
                age = int(data["age"])
                if age < kb["insert_age_old"]:
                    context["age"] = data["age"]
                    return kb, context, {"utt": context["name"] + " " + context["age"],
                                         "BB": False, "FC": True, "FC_c": context["name"] + " " + context["age"]}, True
            except ValueError:
                pass
        return kb, context, {"utt": kb["insert_age_err"]}, False


    # The developer writes a structure that follows ProcessDescriptionInterface with the process description
    my_process = {
        # A list of activities, as specified in ActivityInterface
        # In this example, the process is: insert_name -> insert_age -> print_name_age
        "activities": [
            {"id": "start", "next_id": "insert_name", "type": "START", "evaluate": start},
            {"id": "insert_name", "next_id": "insert_age", "type": "TASK", "evaluate": insert_name},
            {"id": "insert_age", "next_id": "end", "type": "TASK", "evaluate": insert_age},
            {"id": "end", "next_id": None, "type": "END"},
        ],
        "first_activity_id": "start",
        # TODO(giulio) nlu template? "dataTemplate": ["name", "age"],
    }

    # The developer writes a knowledge base, in this case it contains the utterances that are shown to the user when an
    # activities starts, some other utterances, and a constraint on the age.
    my_kb = {
        "start": "welcome",

        "insert_name": "Please insert your name",
        "insert_name_err": "Name not found, please insert your name",

        "insert_age": "Please insert your age",
        "insert_age_err": "The input is not valid, please insert your age",
        "insert_age_old": 100,

        "end": "Process completed!",
    }

    # The initial context is empty, instead of the token, here a callback is forwarded to the framework.
    # The developer creates a framework (which is immediately initialized)
    my_framework = Framework(my_process, my_kb, {}, stupid_nlu)


    # A helper function that extracts the information from the payload of the response and returns an updated state.
    def get_state(response):
        return {
            "BA": "BA" in response and response["BA"],
            "BB": "BB" in response and response["BB"],
            "FC": "FC" in response and response["FC"],
            "FC_c": response["FC_c"] if "FC_c" in response else "empty"
        }


    # The application takes the input from the keyboard and forwards it to the framework, the response is printed out.
    # To quickly simulate a GUI interaction, the application prints BA, BB, FC if the respective elements are visible,
    # and the input "BA" is managed as if the user interacted with BA.
    # The user should insert "BA" only if BA is visible, otherwise the behaviour is not correct.
    # To close the program, the user has to type "quit".
    u_in = ""
    while u_in != "quit":  # TODO(giulio) issues: first "empty" call and how utt are returned
        # handle input and update the state
        if u_in == "BA":
            my_response = my_framework.handle_data_input({"name": "Bob"})
        elif u_in == "BB":
            my_response = my_framework.handle_data_input({"age": "50"})
        else:
            my_response = my_framework.handle_text_input(u_in)
        state = get_state(my_response)

        # print the "GUI"
        if state["BA"]:
            print("BA")
        if state["BB"]:
            print("BB")
        if state["FC"]:
            print("FC:", state["FC_c"])

        # print the "chat panel"
        if "utt" in my_response:
            print("chat:", my_response["utt"])

        # take next input
        u_in = input()
