import json
import brotli

# Step 1: Read base.json
with open('base.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Step 2: Recursively replace "commontext" with "changed text"
def replace_commontext(obj):
    if isinstance(obj, dict):
        return {k: replace_commontext(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_commontext(item) for item in obj]
    elif isinstance(obj, str):
        return obj.replace("commontext", "changed text")
    else:
        return obj

modified_data = replace_commontext(data)

# Step 3: Write to delta.json
with open('delta.json', 'w', encoding='utf-8') as f:
    json.dump(modified_data, f, ensure_ascii=False, indent=2)

# Step 4: Compress delta.json to delta.json.br
with open('delta.json', 'rb') as f_in:
    content = f_in.read()
    compressed = brotli.compress(content)

with open('delta.json.br', 'wb') as f_out:
    f_out.write(compressed)

print("delta.json and delta.json.br generated successfully.")