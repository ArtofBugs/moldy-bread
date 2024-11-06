#! /usr/bin/env python3

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

input_method = None
garble_method = None
output_method = None
plaintext = []

input_handle = None
output_handle = None
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
    global input_method
    global garble_method
    global output_method
    # Some of these symbols may not show up in VSCode depending on the font you're using.

    print("")
    print("**Main menu**")
    print("")
    print("Choose an option by typing its number.")
    print("")

    if input_method is not None:
        print(f"1) Replace input text - ℹ️ currently set: {input_method} ✅")
    else:
        print(f"1) Add input text to be garbled")

    if garble_method is not None:
        print(f"2) Update garbling method - ℹ️ currently selected: {garble_method+1} ✅")
    else:
        print(f"2) Choose garbling method")

    if output_method is not None:
        print(f"3) Update output method - ℹ️ currently selected: {output_method} ✅")
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
    global input_method
    global garble_method
    global output_method
    global garble_ready

    if (
        input_method is not None
        and garble_method is not None
        and output_method is not None
    ):
        garble_ready = True
    else:
        garble_ready = False


def clear_garble_status():
    global input_method
    global garble_method
    global output_method
    global garble_ready
    global plaintext

    input_method = None
    garble_method = None
    output_method = None
    garble_ready = False
    plaintext = []


while True:
    show_menu()
    cmd = input(PROMPT)
    print("")
    if cmd == "1":
        print(
            f"Enter the text to be garbled below. End your input with {color.BOLD}ctrl+d{color.RESET}."
        )
        # Get multiline input until we get EOF - taken from
        # https://stackoverflow.com/a/38223253
        while True:
            try:
                line = input()
            except EOFError:
                break
            plaintext.append(line)

    elif cmd == "2":
        method_index = None
        while method_index is None:
            print(f"Choose a garbling method by typing its number.")
            print("")

            # Print methods
            for i in range(len(GARBLE_METHODS)):
                print(f"{i+1}) {GARBLE_METHODS.keys()[i]}")
            # Additional options (help and exit)
            print(f"{len(GARBLE_METHODS)+1}) What are these? Get help")
            print(f"{len(GARBLE_METHODS)+2}) Exit")
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
                    method_index = None
                elif method_index == len(GARBLE_METHODS) + 1:
                    show_help()
                    method_index = None
                elif method_index == len(GARBLE_METHODS) + 2:
                    break
                else:
                    garble_method = method_index - 1
                    update_garble_status()
                    print("Success!")
    elif cmd == "3":
        update_garble_status()
    elif cmd == "4":
        if garble_ready:
            try:
                subprocess.run(
                    "python3", GARBLE_METHODS[garble_method], stdin=plaintext
                )
                clear_garble_status()
            except Exception as e:
                print(
                    "Failed to garble! Settings have been preserved. This was the encountered error:"
                )
                print(repr(e), sys.stderr)
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
