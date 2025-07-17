# JSONCompressDictDemoSite

This project demonstrates **Compression Dictionary Transport (CDT)** for JSON in the browser, using Chrome Canary’s experimental support.  
Unlike pre-compressed `.zst` or `.br` files, this demo lets the browser negotiate and apply dictionary-based compression on-the-fly, using a previously cached `base.json` as the dictionary for `delta.json`.  
You can observe the dramatic reduction in network transfer size for `delta.json` in Chrome Canary DevTools.

---

## How to Run the Demo

1. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

2. **Generate large JSON files for the demo**
    ```sh
    python createjson.py
    ```
    This will create a large `base.json` and a similar `delta.json` (with a few changes).

3. **Start the server with HTTP/2 and HTTPS (required for CDT)**
    - Generate a self-signed certificate (if you don't have one):
      ```sh
      openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
      ```
    - Start the server with Hypercorn:
      ```sh
      hypercorn serverCDT:app --bind 0.0.0.0:5001 --certfile cert.pem --keyfile key.pem
      ```

4. **Launch Chrome Canary with CDT enabled**
    ```sh
    /Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary --enable-features=CompressionDictionaryTransport
    ```

---

##  Testing Compression Dictionary Transport

1. **Visit** [https://localhost:5001](https://localhost:5001) in Chrome Canary.
2. **Open DevTools → Network tab.**
3. **Hard reload** the page (right-click the reload button → "Empty Cache and Hard Reload").
4. **Observe:**
    - `base.json` is loaded and cached (large, e.g., several MB).
    - `delta.json` is requested after `base.json`.
    - In the **"Transferred"** column, `delta.json` should show a **very small transfer size** (e.g., a few KB or less), even though its uncompressed size is large.
    - The **"Size"** column will show the full uncompressed size after decompression.

**This demonstrates true browser-based dictionary compression, not just pre-compressed file serving!**

---

##  How Dictionary Compression Works Here

- **base.json**: The full reference dataset, sent once and cached by the browser.
- **delta.json**: The updated data (very similar to `base.json`).
- The server sets the `Use-As-Dictionary` header on `delta.json`:
  ```
  Use-As-Dictionary: match="/base.json"
  ```
- Chrome Canary, if CDT is enabled and all requirements are met, will use the cached `base.json` as a dictionary to decompress `delta.json` on-the-fly.

---

##  Project Structure

```
.
├── base.json           # The shared dictionary file (large)
├── delta.json          # The delta file (large, but similar to base.json)
├── createjson.py       # Script to generate large JSON files
├── index.html          # Demo web page (fetches both JSON files)
├── serverCDT.py        # Flask server with correct CDT headers
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

##  Notes

- **No pre-compressed (.zst/.br) files are used or served.**
- **Compression is negotiated and applied by the browser (Chrome Canary) using CDT.**
- **You must use HTTPS and HTTP/2 (Hypercorn with SSL) for CDT to work.**
- **This demo only works as intended in Chrome Canary with the CDT flag enabled.**
- **Other browsers will simply download the full `delta.json` file.**

---

##  References

- [Compression Dictionary Transport (WICG proposal)](https://github.com/WICG/compression-dictionary-transport)
- [Chrome CDT explainer](https://github.com/WICG/compression-dictionary-transport/blob/main/explainer.md)
- [Hypercorn (HTTP/2 Python server)](https://pgjones.gitlab.io/hypercorn/)
