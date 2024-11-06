#! /usr/bin/env python3


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


input_method = None
garble_method = None
output_method = None

input_handle = None
output_handle = None
output_exists = False


def show_welcome():
    welcome_text = f"""
Welcome to {color.BOLD}garbler{color.RESET}!

To garble text, choose input text, a garbling method, and an output method, then
select “Generate garble” to garble the text. Show this help screen at any time
using the “Get help” option.

    """
    print(welcome_text)


def show_menu():
    # Some of these symbols may not show up in VSCode depending on the font you're using.

    print("")
    print("**Main menu**")
    print("")
    print("Choose an option by typing its number.")
    print("")

    if input_method:
        print(f"1) Replace input text - ℹ️ currently set: {input} ✅")
    else:
        print(f"1) Add input text to be garbled")

    if garble_method:
        print(f"2) Update garbling method - ℹ️ currently selected: {garble_method} ✅")
    else:
        print(f"2) Choose garbling method")

    if output_method:
        print("3) Update output method - ℹ️ currently selected: {output} ✅")
        if output_exists:
            print("    (⚠️ warning: this file will be overwritten!)")
    else:
        print("3) Add output method for garbled text")

    if input_method and garble_method and output_method:
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


while True:
    show_menu()
    cmd = input("garbler >> ")
    print("")
    if cmd == "1":
        print(
            f"Enter the text to be garbled below. End your input with {color.BOLD}ctrl+d{color.RESET}."
        )
        # TODO
    elif cmd == "2":
        pass
    elif cmd == "3":
        pass
    elif cmd == "4":
        pass
    elif cmd == "5":
        show_help()
    elif cmd == "6":
        exit(0)
    else:
        print(
            "Command not recognized - please select a menu option by entering a number"
        )
        print("between 1 and 6.")
