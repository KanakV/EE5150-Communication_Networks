# Messenger Client

A simple peer-to-peer messaging client built with Python and Tkinter, communicating with a remote server over HTTP. This project was developed as part of the course EE5150-Communication Networks to demonstrate client-server communication, protocol design, and GUI development.

## Project Overview

This application allows users to send and receive short text messages through a central server. Each user is identified by a numeric ID (1–255), and messages are stored in a server-side buffer until retrieved.

## Project Structure

```
├── config.py                  # Shared configuration and status codes
├── main.py                    # Application entry point (Tkinter GUI)
├── client/
│   ├── userClient.py          # High-level user operations (associate, send, get)
│   └── httpClient.py          # Low-level HTTP communication
└── protocol/
    └── frame.py               # Frame dataclass and serialization
```

## How It Works

### Protocol

Communication between client and server uses a custom **Frame** format sent as JSON over HTTP POST requests. Each frame contains:

| Field     | Description                                      |
|-----------|--------------------------------------------------|
| `type`    | Operation type (`0` = associate, `1` = get, `2` = push) |
| `message` | Command string (e.g. `"ASSOCIATE"`, `"GET"`, `"PUSH"`) |
| `id`      | Sender's user ID                                 |
| `id2`     | Recipient's user ID (for PUSH operations)        |
| `length`  | Payload length in bytes                          |
| `payload` | The message content (max 254 characters)         |

### Status Codes

Defined in `config.py` using a `Status` IntEnum:

| Status            | Meaning                                  |
|-------------------|------------------------------------------|
| `ASSOCIATE_SUCCESS` | Successfully registered with the server |
| `ASSOCIATE_FAIL`    | Registration failed                     |
| `GOT_RESPONSE`      | A message was retrieved from the buffer |
| `EMPTY_BUFFER`      | No messages waiting                     |
| `PUSH_SUCCESS`      | Message delivered to server             |
| `BUFFER_FULL`       | Recipient's buffer is full              |
| `INVALID_LENGTH`    | Message exceeds 254-character limit     |

### Flow

1. **Associate** — The client registers its ID with the server before any messages can be sent or received.
2. **Send** — A `PUSH` frame is sent to the server containing the message and recipient ID.
3. **Receive** — A `GET` frame is sent to poll the server; any queued messages are returned one at a time.

## Getting Started

### Prerequisites

- Python 3.10+
- `requests` library

```bash
pip install requests
```

### Running the App

```bash
python main.py
```

### Usage

1. Enter your user ID (1–255) in the top bar and click **Connect**.
2. Enter a recipient's ID in the left panel and click **Start Chat**.
3. Type a message in the input box and press **Enter** or click **Send**.

## Known Limitations
- The app does not support persistent message history across sessions.
- The server URL is hardcoded in `config.py`.

## Configuration

Edit `config.py` to change these settings:

```python
SERVER_URL = "https://messenger-s0tl.onrender.com/"
TIMEOUT = 5                # HTTP request timeout in seconds
MAX_PAYLOAD_LENGTH = 254   # Maximum message length in characters
```