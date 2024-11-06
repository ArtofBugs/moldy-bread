import json
import sys
import requests

DEBUG = True

words = json.load(sys.stdin)

# if DEBUG:
#     print(words)

for i in range(len(words)):
    new_word = requests.get(f"https://api.datamuse.com/words?rel_jjb={words[i]}").json()
    # new_word = json.load(new_word)
    if new_word != []:
        words[i] = new_word[0]["word"]

print(json.dumps(words))
