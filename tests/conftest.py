"""Test fixtures for the A2A agent tests."""
import pytest
import asyncio
import subprocess
import signal
import sys
import os
from pathlib import Path


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def server(event_loop):
    """Start the server before all tests and stop it after."""
    # Start the server in a subprocess
    server_process = subprocess.Popen(
        [sys.executable, "-m", "server.main"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,  # Create a new process group
    )
    
    # Wait for the server to start
    print("Waiting for server to start...")
    max_retries = 10
    retries = 0
    server_ready = False
    
    while retries < max_retries and not server_ready:
        try:
            # Try to connect to the server
            import httpx
            async with httpx.AsyncClient() as client:
                # Use POST instead of GET to check the agent card
                response = await client.post("http://localhost:9999/", json={}, timeout=1.0)
                if response.status_code in [200, 204, 405]:  # Accept 405 as the server is running but endpoint might differ
                    server_ready = True
                    print("Server is ready!")
        except Exception as e:
            # Wait and retry
            retries += 1
            print(f"Waiting for server to start (attempt {retries}/{max_retries})... Error: {e}")
            await asyncio.sleep(1)
    
    if not server_ready:
        # Kill the server process if it didn't start successfully
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        stdout, stderr = server_process.communicate()
        pytest.fail(f"Server failed to start. Stdout: {stdout.decode()}, Stderr: {stderr.decode()}")
    
    # Wait a bit more to ensure the server is fully initialized
    await asyncio.sleep(1)
    
    # Return the process for later cleanup
    yield server_process
    
    # Cleanup: stop the server after tests
    print("Stopping server...")
    os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
    server_process.wait(timeout=5)
    print("Server stopped.") 