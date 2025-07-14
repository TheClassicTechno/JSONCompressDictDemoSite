import json
import brotlicffi
base = [{"name": "example", "version": "1.0 original"} for i in range(10000)]
delta = [{"name": "example", "version": "1.03 changed"} for i in range(10000)]

with open("base.json", "w") as f:
    json.dump(base, f)

with open("delta.json", "w") as f:
    json.dump(delta, f)

delta_json = json.dumps(delta).encode()
base_json = json.dumps(base).encode()

compressed = brotlicffi.compress(
    data=delta_json,
    # delta_json.encode('utf-8'),
    # mode=brotli.MODE_TEXT,
    quality=11,
    lgwin=22,
    mode=brotlicffi.MODE_TEXT,
    dictionary=base_json
    # dictionary=base_json.encode('utf-8')
)
# compressed.set_dictionary(base_json.encode('utf-8'))
# compressed2= compressed.process(delta_json.encode('utf-8'))
with open("delta.json.br", "wb") as f:
    f.write(compressed)