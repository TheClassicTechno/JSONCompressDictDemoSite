# JSONCompressDictDemoSite

This project demonstrates **dictionary-based compression** for JSON transport using Zstandard (zstd) or Brotli, with a shared dictionary (`base.json`) to efficiently compress a delta file (`delta.json`). The demo runs locally and lets you observe the dramatic reduction in delta size via your browser's DevTools.

---

##  How to Run the Demo

1. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

2. **Start the server**
    ```sh
    python server.py
    ```

3. **(Optional) Install Zstandard or Brotli CLI for compression**
    - For Zstandard:
      ```sh
      brew install zstd
      ```
    - For Brotli:
      ```sh
      brew install brotli
      ```

---

##  Testing Compression Efficiency

1. **Download Chrome Canary** (for experimental dictionary support).
2. **Visit** [http://localhost:5000](http://localhost:5000).
3. **Open DevTools → Network tab.**
4. **Refresh the page and inspect:**
    - `base.json` should be ~4–5 KB (or larger for real data).
    - `delta.json.zst` (or `delta.json.br`) should be **much smaller** (e.g., <1 KB) if dictionary compression is working.
    - `delta.json` (uncompressed) will be similar in size to `base.json`.

**This demonstrates how dictionary-based compression can drastically reduce update payloads.**

---

##  How Dictionary Compression Works Here

- **base.json**: The full reference dataset, sent once and cached by the browser.
- **delta.json**: The updated data (usually very similar to base.json).
- **delta.json.zst**: The delta, compressed using `base.json` as a dictionary.
- The server sets the `Use-As-Dictionary` header to instruct the browser/client to use `base.json` for decompression.

---

##  Compressing delta.json with a Dictionary

### Using Zstandard (zstd):

```sh
zstd --compress --ultra -22 --dict=base.json delta.json -o delta.json.zst
```

### Using Brotli (if supported):

```sh
brotli --input=delta.json --output=delta.json.br --quality=11 --mode=text --dictionary=base.json
```

- The resulting `.zst` or `.br` file will be **much smaller** if `delta.json` is similar to `base.json`.

---

## Project Structure

```
.
├── base.json           # The shared dictionary file
├── delta.json          # The delta file (uncompressed)
├── delta.json.zst      # The delta file, compressed with zstd and base.json as dictionary
├── index.html          # Demo web page
├── server.py           # Flask server to serve files and headers
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

##  How the Demo Works

- The web page fetches `base.json` and `delta.json.zst`.
- You can inspect file sizes in the Network tab.
- The server sets appropriate cache headers and the `Use-As-Dictionary` header for dictionary transport.
- For full benefit, use a browser with experimental dictionary compression support (e.g., Chrome Canary).

---

##  Notes

- **Dictionary compression is most effective when `delta.json` is very similar to `base.json`.**
- If you want even smaller updates, consider sending only a JSON diff/patch instead of a full delta file.
- The demo uses Zstandard (`.zst`) by default, but you can adapt it for Brotli if your toolchain and browser support it.

My JSON Demo Shows Small zst Files on all browsers.
We are serving delta.json.zst as a pre-compressed file.
The .zst file is already compressed on the server using the dictionary (base.json).
Browsers just download the .zst file as-is—they do not need to support Compression Dictionary Transport to see the small file size in the network tab.
The browser is not decompressing or interpreting the file automatically; it just shows the file size as it is served.
Compression Dictionary Transport is about the browser and server negotiating to use a cached file as a dictionary for on-the-fly compression/decompression.
Pre-compressed files (like .zst) are always small, regardless of browser support, because the compression already happened on the server.


---

##  References

- [Zstandard Dictionary Compression](https://facebook.github.io/zstd/)
- [Brotli Compression](https://github.com/google/brotli)
- [Chrome Dictionary Compression Proposal](https://github.com/WICG/compression-dictionary-transport)

---
