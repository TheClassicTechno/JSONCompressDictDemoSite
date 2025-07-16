# JSONCompressDictDemoSite
This project demonstrates Brotli compression using a shared dictionary (base.json) to significantly reduce the size of a delta file (delta.json). The site runs locally and allows you to observe efficient compression via DevTools.

# How to Run the Demo
1. Install dependencies

pip install -r requirements.txt
2. Start the server

python server.py

# Testing Compression Efficiency
Step-by-step:
Download Chrome Canary (to test custom Brotli dictionary support).

Visit http://localhost:5000.

Open DevTools → Network tab.

Refresh the page and inspect:

base.json should be ~410 KB

delta.json.br should be < 10 KB

This showcases dictionary-based compression in action.

# Brotli Dictionary Compilation
To build the Brotli encoder and use it with a dictionary:

Clone and build Brotli:
git clone https://github.com/google/brotli
cd brotli
mkdir out && cd out
cmake ..
make -j4
# Compile the Dictionary Compression Script
Assuming Brotli headers and libs are available after build:

g++ compress_with_dict.cpp \
    -I../include \
    -L../out \
    -lbrotlienc \
    -o compress_dict
If you installed Brotli system-wide:

g++ compress_with_dict.cpp \
    -lbrotlienc \
    -o compress_dict
Or specify all include paths manually:

g++ compress_dict.cpp \
    -I./brotli/c/include \
    -L./brotli/out \
    -lbrotlienc \
    -o compress_dict
# Run the Compressor
./compress_dict
This generates delta.json.br, compressed using base.json as the dictionary.

# Summary

Demonstrates dictionary-based Brotli compression

Provides a visual web interface

Uses minimal Python and C++ code for integration

