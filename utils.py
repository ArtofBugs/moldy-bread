from textwrap import fill


def print_wrapped(text):
    print(fill(text, 80, break_on_hyphens=False))
