# Garbler

You have a message, and you want to change it into a different one
that sounds like gibberish but *kind of* means the same thing in a fuzzy way...

A silly CLI program that will substitute words in an input text
with other, tangentially-related words!

## Setup

To use `garbler` for yourself, download and set it up using these steps:

1. Clone the repository and submodules.

    ```sh
    $ git clone https://github.com/ArtofBugs/moldy-bread.git
    $ cd moldy-bread
    $ git submodule init
    $ git submodule update
    ```

1. Make a virtual environment and install the Python dependencies.

    ```sh
    $ python3 -m venv .venv
    $ pip install -r requirements.txt
    ```

1. Install the dependencies for the Node microservices.

    ```sh
    $ cd microservices
    $ npm install
    $ cd ..
    ```

1. Start the main program.

    ```sh
    $ ./main.py
    ```

1. Start the substring replacer microservice.

    ```sh
    $ python3 substring_replacer.py
    ```

1. Start the Node microservices.

    ```sh
    # Run for each microservice file
    $ node <name>_microservice.js
    ```

## Usage

Select options by entering the number next to it in the menu at the prompt.
Read the help menu for more information on individual options.
