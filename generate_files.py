import json

base = [{"name": "example", "version": "1.0 original"} for i in range(10000)]
delta = [{"name": "example", "version": "1.03 changed"} for i in range(10000)]

with open("base.json", "w") as f:
    json.dump(base, f)

with open("delta.json", "w") as f:
    json.dump(delta, f)

print("Now run this command in your terminal to compress delta.json with base.json as dictionary:")
print("brotli -Z -D base.json -o delta.json.br delta.json")