#! /usr/bin/env python3

import json
import os.path
import subprocess
import sys

import nltk
from indexed import IndexedOrderedDict


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
        "Synonyms": "synonym_microservice.py",
        "Adjectives": "adjective_microservice.py",
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
    welcome_text = f"""
Welcome to {color.BOLD}garbler{color.RESET}!

To garble text, choose input text, a garbling method, and an output method, then
select “Generate garble” to garble the text. Show this help screen at any time
using the “Get help” option.

    """
    print(welcome_text)


def show_menu():
    global plaintext
    global garble_method
    global output_file
    # Some of these symbols may not show up in VSCode depending on the font you're using.

    print("")
    print("**Main menu**")
    print("")
    print("Choose an option by typing its number.")
    print("")

    if plaintext is not None:
        print(f"1) Replace input text - ℹ️ currently set: Standard input ✅")
    else:
        print(f"1) Add input text to be garbled")

    if garble_method is not None:
        print(f"2) Update garbling method - ℹ️ currently selected: {garble_method+1} ✅")
    else:
        print(f"2) Choose garbling method")

    if output_file is not None:
        print(
            f"3) Update output method - ℹ️ currently selected: {'Standard output' if output_file == '' else output_file} ✅"
        )
        if output_exists:
            print("    (⚠️ warning: this file will be overwritten!)")
    else:
        print("3) Add output method for garbled text")

    if garble_ready:
        print("4) Generate garble ✅")
    else:
        print("4) Generate garble ❌")

    print("5) Get help")
    print("6) Exit")

    print("")


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


while True:
    show_menu()
    cmd = input(PROMPT)
    print("")

    if cmd == "1":
        plaintext = ""
        print(
            f"Enter the text to be garbled below. End your input with {color.BOLD}ctrl+d{color.RESET}."
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

    elif cmd == "2":
        while True:
            print(f"Choose a garbling method by typing its number.")
            print("")

            # Print methods
            for i in range(len(GARBLE_METHODS)):
                print(f"{i+1}) {GARBLE_METHODS.keys()[i]}")
            # Additional options (help and exit)
            print(f"{len(GARBLE_METHODS)+1}) What are these? Get help")
            print(f"{len(GARBLE_METHODS)+2}) Return to main menu")
            print("")

            method_chosen = input(PROMPT)

            print("")
            if not method_chosen.isdigit():
                print(
                    f"""
Option not recognized - please select a garbling option by entering a number
between 1 and {len(GARBLE_METHODS)}, get help by entering {len(GARBLE_METHODS)+1},
or return to the main menu by entering {len(GARBLE_METHODS)+2}.
                """
                )
            else:
                method_index = int(method_chosen)
                if method_index > len(GARBLE_METHODS) + 2 or method_index < 1:
                    print(
                        f"Option not recognized - please enter an option number between 1 and {len(GARBLE_METHODS)+2}."
                    )
                elif method_index == len(GARBLE_METHODS) + 1:
                    show_help()
                elif method_index == len(GARBLE_METHODS) + 2:
                    break
                else:
                    garble_method = method_index - 1
                    update_garble_status()
                    print("Success!")
                    break
    elif cmd == "3":
        while True:
            print(f"Choose an output method by typing its number.")
            print("")

            print("1) Standard output")
            print("2) File output")
            print("3) Get help")
            print("4) Return to main menu")
            print("")

            method_chosen = input(PROMPT)
            print("")

            if not method_chosen.isdigit():
                print(
                    f"""
Option not recognized - please select an output option by entering a number
between 1 and 2, get help by entering 3, or return to the main menu by entering
4.
                """
                )
            else:
                method_index = int(method_chosen)
                if method_index == 1:
                    output_file = ""
                    print("Success!")
                    break
                elif method_index == 2:
                    while True:
                        file_path = input("Enter a path to the file: ")
                        print("")

                        if os.path.isfile(file_path):
                            print("File found!")
                            print("")
                            print(
                                f"{color.BOLD}Warning: This file will be overwritten. Are you sure you want to select it?{color.RESET}"
                            )
                            print("")
                            print("1) Yes, that's fine.")
                            print("2) Nope, choose a different one!")
                            print("")

                            file_ok = input(PROMPT)
                            print("")

                            if file_ok == "1":
                                output_file = file_path
                                print("Success!")
                                break

                        else:
                            output_file = file_path
                            print("Success!")
                            break
                    break
                elif method_index == 3:
                    show_help()
                elif method_index == 4:
                    break
                else:
                    print(
                        f"Option not recognized - please enter an option number between 1 and 4."
                    )
        update_garble_status()
    elif cmd == "4":
        if garble_ready:
            tokens = nltk.word_tokenize(plaintext, preserve_line=True)
            try:
                # print(GARBLE_METHODS.values()[garble_method])
                # print(json.dumps(tokens))
                result = subprocess.run(
                    ["python3", GARBLE_METHODS.values()[garble_method]],
                    input=json.dumps(tokens),
                    encoding="ascii",
                    stdout=subprocess.PIPE,
                )
                result = json.loads(result.stdout)
            except Exception as e:
                print(
                    "Failed to garble! Settings have been preserved. This was the encountered error:"
                )
                print(repr(e), sys.stderr)
                continue
            if output_file != "":
                with open(output_file, "w") as f:
                    for token in result:
                        f.write(token)
                        f.write(" ")
            else:
                for token in result:
                    print(token, sep=" ")
                print("")
            print("Success!")
        else:
            print(
                """
Can't choose this option yet! Check that you have added input text, chosen a
garbling method, and added an output method!
                """
            )

    elif cmd == "5":
        show_help()
    elif cmd == "6":
        exit(0)
    else:
        print(
            """
Command not recognized - please select a menu option by entering a number
between 1 and 6.
            """
        )
