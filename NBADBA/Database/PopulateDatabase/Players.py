import requests
import json

with open("players.txt", "rb") as fin:
    content = json.load(fin)
print content[resultSets]
