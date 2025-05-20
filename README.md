# A2A Experiment agent

A simple A2A (Agent-to-Agent) protocol implementation that shows skeleton of such agents.

## Overview

This project demonstrates:
- A minimal A2A server implementation
- Proper package structure for server components
- Docker containerization
- Automated testing with pytest

## Project Structure

```
experiment-agent/
├── server/              # Server implementation
│   ├── __init__.py      # Package initialization
│   ├── main.py          # Server entry point
│   └── agent_executor.py # Agent implementation
├── tests/               # Test suite
│   ├── __init__.py
│   ├── conftest.py      # Test fixtures
│   └── test_simple.py   # Tests for server
├── Dockerfile           # Docker configuration
└── pyproject.toml       # Project dependencies
```

## Setup

This project uses `uv` for dependency management.

1. Make sure you have `uv` installed
2. Install dependencies:
   ```
   uv sync
   ```
3. Install development dependencies:
   ```
   uv pip install -e ".[dev]"
   ```

## Running the Agent

### Using uv

Start the A2A server:

```
uv run -m server.main
```

This will start the agent server on http://localhost:9999.

### Using Docker

Build and run the Docker container:

```bash
# Build the Docker image
docker build -t a2a-server .

# Run the container
docker run -p 9999:9999 a2a-server
```

This will start the agent server in a container, accessible at http://localhost:9999.

## Testing

Run the test suite with:

```
uv run -m pytest
```

This will:
1. Start the server in a subprocess
2. Run tests against the running server
3. Automatically shut down the server when tests complete

## A2A Protocol

This implementation follows the [Agent-to-Agent (A2A) Protocol](https://google.github.io/A2A/), which is an open protocol for agent-to-agent communication developed by Google.

### Key Features

- RESTful API using JSON-RPC
- Support for both streaming and non-streaming responses
- Agent card provides metadata and capabilities

## API Endpoints

- `POST /`: Get agent card or send messages
- Agent responds with "Hello World" to any text input

## Development

To develop and extend this agent:

1. Modify `server/agent_executor.py` to change agent behavior
2. Add new tests in the `tests/` directory
3. Run tests to verify your changes
4. Build and test the Docker image for deployment
