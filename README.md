# main_program_361

A small **Python microservice** that looks up author information (birth date + bio) from **Open Library** and serves the result over **ZeroMQ**.

## What it does

- Accepts a JSON request over ZeroMQ (REP socket)
- Searches Open Library for an author name
- Fetches that author’s details
- Returns a JSON response containing:
  - `birth_date`
  - `bio`

## Requirements

- Python 3.9+ (3.8+ should work)
- Network access to `openlibrary.org`

Python packages:
- `pyzmq`
- `requests`

Install dependencies:

```bash
pip install pyzmq requests
```

## Running the service

The microservice code is in `AuthorInfo.py`.

Start it:

```bash
python AuthorInfo.py
```

By default it binds to:

- `tcp://*:5556`

You should see:

```
AuthorInfo Microservice is running on port 5556...
```

## Request / Response format

### Request

Send JSON shaped like:

```json
{
  "request": {
    "id": "req-1",
    "author": "Isaac Asimov"
  }
}
```

- `request.id` is echoed back so clients can correlate responses.
- `request.author` is the author name to search.

### Success response

```json
{
  "api_type": "AUTHOR_INFO",
  "status": "success",
  "author_info": {
    "id": "req-1",
    "birth_date": "1920",
    "bio": "..."
  }
}
```

### Error response

If the author can’t be found or the API call fails, you’ll get:

```json
{
  "api_type": "AUTHOR_INFO",
  "status": "error",
  "response": {
    "id": "req-1",
    "error": "Author '...' not found in Open Library"
  }
}
```

## Example client

Here is a minimal ZeroMQ client to test the service.

```python
import zmq

ctx = zmq.Context()
sock = ctx.socket(zmq.REQ)
sock.connect("tcp://localhost:5556")

sock.send_json({
    "request": {
        "id": "req-1",
        "author": "Isaac Asimov"
    }
})

print(sock.recv_json())
```

## Notes / Implementation details

- The search uses Open Library’s author search endpoint:
  - `https://openlibrary.org/search/authors.json?q=<author>`
- It then fetches details from:
  - `https://openlibrary.org/authors/<key>.json`
- `bio` in Open Library can be either a string or an object; this service normalizes it to a string.

## Troubleshooting

- **Timeouts / connection errors**: confirm you have internet access and Open Library is reachable.
- **Port already in use**: change the bind port in `AuthorInfo.py` (`socket.bind("tcp://*:5556")`).

## License

No license file is currently included in this repository. If you plan to share or reuse this code, consider adding a `LICENSE` file (for example MIT, Apache-2.0, or GPL-3.0).
