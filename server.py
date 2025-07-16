from flask import Flask, send_from_directory, Response, make_response
from datetime import datetime, timedelta
import os

app = Flask(__name__)

def cache_response(resp, max_age=3600):
    """Add strong caching headers to a response."""
    now = datetime.utcnow()
    expire_time = now + timedelta(seconds=max_age)
    resp.headers['Cache-Control'] = f'public, max-age={max_age}'
    resp.headers['Expires'] = expire_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    resp.headers['Date'] = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return resp

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route("/base.json")
def base_json():
    resp = make_response(send_from_directory('.', 'base.json'))
    return cache_response(resp, max_age=86400)  # 1 day cache

@app.route("/delta.json.zst")
def delta_json_zst():
    with open('delta.json.zst', 'rb') as f:
        compressed_data = f.read()
    resp = Response(compressed_data, mimetype='application/json')
    resp.headers['Content-Encoding'] = 'zstd'
    resp.headers['Use-As-Dictionary'] = 'match="base.json"'  # required by browser spec
    return cache_response(resp, max_age=3600)  # 1 hour cache

if __name__ == "__main__":
    app.run(debug=True)



# from flask import Flask, send_from_directory, Response, make_response
# from datetime import datetime, timedelta

# app = Flask(__name__)

# def cache_response(resp, max_age=3600):
#     """Add cache headers to a response object."""
#     resp.headers['Cache-Control'] = 'public, max-age={}'.format(max_age)

#     expire_time = datetime.utcnow() + timedelta(seconds=max_age)
#     resp.headers['Expires'] = expire_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
#     return resp

# @app.route('/')
# def index():
#     return send_from_directory('.', 'index.html')

# @app.route("/base.json")
# def base_json():
#     resp = make_response(send_from_directory('.', 'base.json'))
#     return cache_response(resp, max_age=86400)  # cache dictionary for 1 day

# @app.route("/delta.json.zst")
# def delta_json_zst():
#     with open('delta.json.zst', 'rb') as f:
#         compressed_data = f.read()
#     resp = Response(compressed_data, mimetype='application/json')
#     resp.headers['Content-Encoding'] = 'zstd'
#     resp.headers['Use-As-Dictionary'] = 'base.json'
#     return cache_response(resp, max_age=3600)  # cache delta for 1 hour

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, send_from_directory, Response

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return send_from_directory('.', 'index.html')

# @app.route("/base.json")
# def base_json():
#     return send_from_directory('.', 'base.json')

# @app.route("/delta.json.br")
# def delta_json_br():
#     with open('delta.json.br', 'rb') as f:
#         compressed_data = f.read()
#     headers = {
#         "Content-Encoding": "br",
#         'Content-Type': 'application/json'
#     }
#     return Response(compressed_data, headers=headers)

# @app.route("/delta.json")
# def delta_json():
#     with open('delta.json.br', 'rb') as f:
#         compressed_data = f.read()
#     headers = {
#         "Content-Encoding": "br",
#         'Content-Type': 'application/json',
#         'Use-As-Dictionary': 'base.json'
#     }
#     return Response(compressed_data, headers=headers)

# if __name__ == "__main__":
#     app.run(debug=True)
