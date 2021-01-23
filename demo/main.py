import tkinter as tk
import os.path

from examples.demo.my_callbacks import get_callback
from mmcc_framework import Framework, RasaNlu


# A helper function that extracts the information from the payload of the response and returns an updated state.
def get_state(response, old_state):
    response = response["payload"]
    return {
        "show_name": response["show_name"] if "show_name" in response else old_state["show_name"],
        "show_age": response["show_age"] if "show_age" in response else old_state["show_age"],
        "show_choose_name": response["show_choose_name"] if "show_choose_name" in response else old_state[
            "show_choose_name"],
        "show_choose_nickname": response["show_choose_nickname"] if "show_choose_nickname" in response else old_state[
            "show_choose_nickname"],
        "show_field": response["show_field"] if "show_field" in response else old_state["show_field"],
        "field_contents": response["field_contents"] if "field_contents" in response else old_state["field_contents"],
    }


# A frame with some buttons and a chat.
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Prepare the state and the framework.
        self.state = {"show_name": False, "show_age": False, "show_choose_name": False, "show_choose_nickname": False,
                      "show_field": False, "field_contents": ""}
        self.framework = Framework.from_file("my_process.json",
                                             "my_kb.json",
                                             {},
                                             get_callback,
                                             RasaNlu(os.path.join("rasa_model", "nlu")))
        self.master = master
        self.pack()

        # Add the buttons.
        self.name_button = tk.Button(self.master, text='Insert "Bob"', command=lambda: self.send_data({"name": "Bob"}))
        self.name_button.pack()
        self.age_button = tk.Button(self.master, text='Insert "50"', command=lambda: self.send_data({"age": "50"}))
        self.age_button.pack()
        self.choose_name_button = tk.Button(self.master, text="Use the name",
                                            command=lambda: self.send_data({"name_nickname": "name"}))
        self.choose_name_button.pack()
        self.choose_nickname_button = tk.Button(self.master, text="Use the nickname",
                                                command=lambda: self.send_data({"name_nickname": "nickname"}))
        self.choose_nickname_button.pack()
        self.field = tk.Label(self.master, text="")
        self.field.pack()

        # Add the chat.
        self.chat = tk.Text(self.master, state=tk.constants.DISABLED)
        self.chat.tag_config('user_input', foreground="blue")
        self.chat.pack()
        self.insert = tk.Text(self.master, wrap='none', height=1)
        self.insert.pack()

        # The user can send the text input either pressing the button or pressing Return.
        self.go = tk.Button(self.master, text="ENTER", command=self.send_text)
        self.master.bind('<Return>', self.send_text)
        self.go.pack()

        # Update the view
        self.update_view(self.framework.handle_text_input(""))

    # Updates the view using the state.
    def update_view(self, response):
        self.chat["state"] = tk.constants.NORMAL
        self.chat.insert(tk.constants.END, "\n" + response["utterance"])
        self.chat["state"] = tk.constants.DISABLED
        self.state = get_state(response, self.state)

        self.name_button['state'] = (tk.constants.NORMAL if self.state["show_name"] else tk.constants.DISABLED)
        self.age_button["state"] = tk.constants.NORMAL if self.state["show_age"] else tk.constants.DISABLED
        self.choose_name_button["state"] = tk.constants.NORMAL if self.state[
            "show_choose_name"] else tk.constants.DISABLED
        self.choose_nickname_button["state"] = tk.constants.NORMAL if self.state[
            "show_choose_nickname"] else tk.constants.DISABLED
        self.field["state"] = tk.constants.NORMAL if self.state["show_field"] else tk.constants.DISABLED
        self.field["text"] = self.state["field_contents"]

    def send_data(self, data):
        self.update_view(self.framework.handle_data_input(data))

    def send_text(self, event=None):
        text = self.insert.get('1.0', 'end-1c')
        self.insert.delete('1.0', tk.constants.END)
        self.chat["state"] = tk.constants.NORMAL
        self.chat.insert(tk.constants.END, "\n-- " + text, "user_input")
        self.chat["state"] = tk.constants.DISABLED
        response = self.framework.handle_text_input(text)
        self.update_view(response)


# Run the app.
if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
