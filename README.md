# MMCC - MultiModal Chatbot Creator

This project is based on the paper "A Conceptual Framework for Multi-modal Process-driven Conversational Agents".
It provides a framework that, if kept updated with the inputs from the user, guides him through an appropriately defined process, regardless of the input type.

The framework provides the core functionalities, it is a python package that can be used in any application.
The frontend provides an implementation of React components that use the framework via a backend.

* [frontend](frontend/src/react-mmcc/README.md) documentation
* [backend](backend/README.md) documentation
* [framework](framework/README.md) documentation

## Docker example

To run the Docker example:

* Download and install [Docker](https://www.docker.com/)
* Clone this repo: `git clone https://github.com/giubots/MultimodalChatbotCreator.git`
* From the root directory of the repo run `docker-compose up -d`
* A MMCC backend with the example process is now running on port `8765`!
* You can connect to the example page on `localhost:3000`
* To stop the example, run `docker-compose down`

## How to use

To use MMCC in your project:

* Use the frontend React components in your web page.
* Prepare the `my_process.json`, `my_kb.json` and `my_callbacks.py` files;
  instructions on how to write this files is available in the [framework](framework/README.md) documentation.
* If you need to perform NLU, train a [Rasa](https://rasa.com/) model accordingly with your callbacks.
* Install [Docker](https://www.docker.com/).
* Download and edit the docker-compose [script](./docker-compose.yml) to include your configuration files and model.
* Run `docker-compose up -d` to start the containers with Rasa and MMCC.
* A MMCC backend configured with your process is now running on port `8765`!
