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

# Step 4: Read files as bytes
with open('delta.json', 'rb') as f_delta, open('base.json', 'rb') as f_dict:
    delta_bytes = f_delta.read()
    dict_bytes = f_dict.read()

# Step 5: Compress using Brotli with base.json as dictionary
compressed = brotli.compress(
    delta_bytes,
    quality=11,
    mode=brotli.MODE_TEXT,
    dictionary=dict_bytes
)

# Step 6: Save compressed output
with open('delta.json.br', 'wb') as f_out:
    f_out.write(compressed)

print("✅ delta.json and delta.json.br generated successfully using Brotli with dictionary compression.")
