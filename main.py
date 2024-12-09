#! /usr/bin/env python3

import json
import os.path
import time

import nltk
from indexed import IndexedOrderedDict
import requests

from utils import print_wrapped


# Inspired by https://stackoverflow.com/a/17303428
# ANSI color codes reference here:
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#8-16-colors
class color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


GARBLE_METHODS = IndexedOrderedDict(
    {
        "Synonyms": 8000,
        "Adjectives": 8001,
        "Similar-sounding words": 8002,
        "Words after": 8003,
        "Substrings": None,
    }
)

PROMPT = "garbler >> "

garble_method = None
plaintext = None
garbled_text = ""

input_handle = None
output_file = None
output_exists = False

garble_ready = False


def show_welcome():
    welcome_text = (
        f"Welcome to {color.BOLD}garbler{color.RESET}! To garble text, "
        "choose input text, a garbling method, and an output method, "
        "then select “Generate garble” to garble the text. "
        "Show this help screen at any time using the “Get help” option."
    )
    print_wrapped(welcome_text)


def show_menu():
    update_garble_status()

    global plaintext
    global garble_method
    global output_file
    # Some of these symbols may not show up in VSCode depending on the font you're using.

    print_wrapped("")
    print_wrapped("**Main menu**")
    print_wrapped("")
    print_wrapped("Choose an option by typing its number.")
    print_wrapped("")

    if plaintext is not None:
        print_wrapped(f"1) Replace input text - ℹ️ currently set: Standard input ✅")
    else:
        print_wrapped(f"1) Add input text to be garbled")

    if garble_method is not None:
        print_wrapped(
            f"2) Update garbling method - ℹ️ currently selected: {garble_method+1} ✅"
        )
    else:
        print_wrapped(f"2) Choose garbling method")

    if output_file is not None:
        print_wrapped(
            f"3) Update output method - ℹ️ currently selected: "
            f"{'Standard output' if output_file == '' else output_file} ✅"
        )
        if output_exists:
            print_wrapped("    (⚠️ warning: this file will be overwritten!)")
    else:
        print_wrapped("3) Add output method for garbled text")

    if garble_ready:
        print_wrapped("4) Generate garble ✅")
    else:
        print_wrapped("4) Generate garble ❌")

    print_wrapped("5) Get help")
    print_wrapped("6) Exit")

    print_wrapped("")


def show_help():
    help_text = f"""

{color.BOLD}garbler{color.RESET} can garble text for you!

At each prompt, enter the number corresponding with the option you'd like to
choose.

{color.UNDERLINE}Quick start{color.RESET}:

To garble text, choose input text, a garbling method, and an output method,
then select “Generate garble” to garble the text. Show this help screen at any
time using the “Get help” option.

{color.UNDERLINE}Option details{color.RESET}:

Input methods:
Standard input - enter input text by typing it into the shell. End entry at any
time using {color.BOLD}ctrl+d{color.RESET}.

File input - choose a file that contains the input text.

Garbling methods:
Synonyms - replace as many words as possible in the input text with synonyms.

Adjectives - replace as many words as possible in the input text with an
             adjective that is often used to describe it.

Similar-sounding words - replace as many words as possible in the input text
                         with another word that sounds similar.

Words after - replace as many words as possible in the input text with another
              word that commonly comes after it in a sentence.

Substrings - replace as many words as possible in the input text with another
             word that contains the original word as a substring.

Output methods:
Standard output - garbled text will be printed out into the shell.

File output - choose a file to write the garbled text to. If the provided file
name doesn't yet exist, it will be created. If the provided file name already
exists, {color.BOLD}it will be overwritten{color.RESET}. Please choose wisely!

    """

    print(help_text)


def update_garble_status():
    global plaintext
    global garble_method
    global output_file
    global output_exists
    global garble_ready

    if plaintext is not None and garble_method is not None and output_file is not None:
        garble_ready = True

        if os.path.isfile(output_file):
            output_exists = True
        else:
            output_exists = False
    else:
        garble_ready = False


def clear_garble_status():
    global plaintext
    global garble_method
    global output_file
    global garble_ready

    plaintext = None
    garble_method = None
    output_file = None
    garble_ready = False

clear_garble_status()
show_welcome()
while True:
    show_menu()
    cmd = input(PROMPT)
    print_wrapped("")

    if cmd == "1":
        plaintext = ""
        print_wrapped(
            "Enter the text to be garbled below. "
            f"End your input with {color.BOLD}ctrl+d{color.RESET}."
        )
        # Get multiline input until we get EOF - inspired by
        # https://stackoverflow.com/a/38223253
        while True:
            try:
                line = input()
            except EOFError:
                break
            plaintext += line
            plaintext += "\n"

        print_wrapped("")
        print_wrapped("Success!")

    elif cmd == "2":
        while True:
            print_wrapped(f"Choose a garbling method by typing its number.")
            print_wrapped("")

            # Print methods
            for i in range(len(GARBLE_METHODS)):
                print_wrapped(f"{i+1}) {GARBLE_METHODS.keys()[i]}")
            # Add additional options (help and exit)
            print_wrapped(f"{len(GARBLE_METHODS)+1}) What are these? Get help")
            print_wrapped(f"{len(GARBLE_METHODS)+2}) Return to main menu")
            print_wrapped("")

            method_chosen = input(PROMPT)

            print_wrapped("")
            if not method_chosen.isdigit():
                print_wrapped(
                    "Option not recognized - please select a garbling option "
                    "by entering a number between "
                    f"1 and {len(GARBLE_METHODS)},"
                    f" get help by entering {len(GARBLE_METHODS)+1},"
                    f" or return to the main menu by entering"
                    f" {len(GARBLE_METHODS)+2}."
                )
            else:
                method_index = int(method_chosen)
                if method_index > len(GARBLE_METHODS) + 2 or method_index < 1:
                    print_wrapped(
                        "Option not recognized - please enter "
                        "an option number between 1 and "
                        f"{len(GARBLE_METHODS)+2}."
                    )
                elif method_index == len(GARBLE_METHODS) + 1:
                    show_help()
                elif method_index == len(GARBLE_METHODS) + 2:
                    break
                else:
                    garble_method = method_index - 1
                    print_wrapped("Success!")
                    break
    elif cmd == "3":
        while True:
            print_wrapped(f"Choose an output method by typing its number.")
            print_wrapped("")

            print_wrapped("1) Standard output")
            print_wrapped("2) File output")
            print_wrapped("3) Get help")
            print_wrapped("4) Return to main menu")
            print_wrapped("")

            method_chosen = input(PROMPT)
            print_wrapped("")

            if not method_chosen.isdigit():
                print_wrapped(
                    "Option not recognized - please select an output option "
                    "by entering a number between 1 and 2, "
                    "get help by entering 3, or return to the main menu "
                    "by entering 4."
                )
            else:
                method_index = int(method_chosen)
                if method_index == 1:
                    output_file = ""
                    print_wrapped("Success!")
                    break
                elif method_index == 2:
                    while True:
                        file_path = input("Enter a path to the file: ")
                        print_wrapped("")

                        if os.path.isfile(file_path):
                            print_wrapped("File found!")
                            print_wrapped("")
                            print_wrapped(
                                f"{color.BOLD}Warning: "
                                "This file will be overwritten. "
                                "Are you sure you want to select it?"
                                "{color.RESET}"
                            )
                            print_wrapped("")
                            print_wrapped("1) Yes, that's fine.")
                            print_wrapped("2) Nope, choose a different one!")
                            print_wrapped("")

                            file_ok = input(PROMPT)
                            print_wrapped("")

                            if file_ok == "1":
                                output_file = file_path
                                print_wrapped("Success!")
                                break

                        else:
                            output_file = file_path
                            print_wrapped("Success!")
                            break
                    break
                elif method_index == 3:
                    show_help()
                elif method_index == 4:
                    break
                else:
                    print_wrapped(
                        f"Option not recognized - please enter "
                        "an option number between 1 and 4."
                    )
    elif cmd == "4":
        if garble_ready:
            try:
                tokens = nltk.word_tokenize(plaintext, preserve_line=True)
                result = []
                if garble_method == len(GARBLE_METHODS) - 1:
                    # Use Microservice A
                    # (the substring-replacer-microservice submodule by FlintSable)
                    INPUT_FILE = (
                        "microservices/substring-replacer-microservice/input.json"
                    )
                    with open(INPUT_FILE, "w") as f:
                        json.dump({"status": "pending", "words": tokens}, f, indent=2)
                    while True:
                        with open(INPUT_FILE, "r") as f:
                            result = json.load(f)
                        if result.get("status") == "completed":
                            result = result["replacements"].values()
                            break
                        time.sleep(3)
                else:
                    result = requests.post(
                        url=f"http://localhost:{GARBLE_METHODS.values()[garble_method]}",
                        json=tokens,
                    )
                    result = result.json()
            except Exception as e:
                print_wrapped(
                    "Failed to garble! Settings have been preserved. "
                    "This was the encountered error:"
                )
                print_wrapped(e)
                continue
            if output_file != "":
                with open(output_file, "w") as f:
                    for token in result:
                        f.write(token)
                        f.write(" ")
            else:
                print(*result, sep=" ")
                print_wrapped("")
            print_wrapped("Success!")
        else:
            print_wrapped(
                "Can't choose this option yet! Check that you have "
                "added input text, chosen a garbling method, and "
                "added an output method!"
            )

    elif cmd == "5":
        show_help()
    elif cmd == "6":
        exit(0)
    else:
        print_wrapped(
            "Command not recognized - please select a menu option by "
            "entering a number between 1 and 6."
        )
