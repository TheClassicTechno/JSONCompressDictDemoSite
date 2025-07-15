# JSONCompressDictDemoSite

instructions to run

## pip install -r requirements.txt

## python server.py

## http://localhost:5000

## you will see a link to download base.json and delta.json (compressed with brotli using base as dictionary)

# testing compression dictionary transport

## download chrome canary, visit localhost:5000, open DevTools->Network to observe sizes of base.json and delta.json being downloaded efficiently

should be ueeing base.json as 410 KB and delta.json as <10KB

git clone https://github.com/google/brotli
cd brotli
mkdir out && cd out
cmake ..
make -j4


# Compile the script
Assuming Brotli headers and libs are available after build:

g++ compress_with_dict.cpp -I../include -L../out -lbrotlienc -o compress_dict
Or if you installed Brotli system-wide:

g++ compress_with_dict.cpp -lbrotlienc -o compress_dict
# Run it

./compress_dict
This will generate a delta.json.br compressed using base.json as dictionary.

