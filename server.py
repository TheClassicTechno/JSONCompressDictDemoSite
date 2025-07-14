from flask import Flask, request, jsonify, send_from_directory, render_template, Response

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route("/base.json")
def base_json():
    return send_from_directory('.', 'base.json')

@app.route("/delta.json")
def delta_json():
    with open('delta.json.br', 'rb') as f:
        compressed_data = f.read()
    headers = {
            "Content-Encoding": "br",
            'Content-Type': 'application/json',
            'Use-As-Dictionary': 'base.json'
    }
    return Response(compressed_data, headers=headers)

if __name__ == "__main__":
    app.run(debug=True)
