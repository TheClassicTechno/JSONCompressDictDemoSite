import json
import random

N = 10000  # Number of objects (increase for even larger files)

# Generate base.json: lots of repeated structure and text
base = [
    {
        "id": i,
        "name": "item",
        "desc": "common text " * 10,
        "details": {
            "category": "A",
            "info": "lorem ipsum dolor sit amet " * 5,
            "tags": ["alpha", "beta", "gamma"]
        }
    }
    for i in range(N)
]

# Generate delta.json: mostly the same, but a few changes
delta = []
for i, obj in enumerate(base):
    new_obj = obj.copy()
    if i % 1000 == 0:  # Change every 1000th entry
        new_obj["desc"] = "changed text " * 10
        new_obj["details"]["info"] = "DIFFERENT info " * 5
        new_obj["details"]["tags"] = ["delta", "epsilon"]
    delta.append(new_obj)

with open("base.json", "w") as f:
    json.dump(base, f, indent=0)

with open("delta.json", "w") as f:
    json.dump(delta, f, indent=0)

print("Generated large base.json and delta.json!")