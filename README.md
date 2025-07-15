# JSONCompressDictDemoSite

instructions to run

## pip install -r requirements.txt

## python server.py

## http://localhost:5000

## you will see a link to download base.json and delta.json (compressed with brotli using base as dictionary)

# testing compression dictionary transport

## download chrome canary, visit localhost:5000, open DevTools->Network to observe sizes of base.json and delta.json being downloaded efficiently

should be ueeing base.json as 410 KB and delta.json as <10KB


****git clone https://github.com/google/brotli
cd brotli
mkdir out && cd out
cmake ..
make -j4
****
