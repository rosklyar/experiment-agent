FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Install git for dependencies from Git repositories
RUN apt-get update && apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the entire project
COPY server/ ./server/
COPY pyproject.toml .

# Sync the project into a new environment
RUN uv sync

# Expose the port
EXPOSE 9999

# Run using the Python from the virtual environment
CMD ["uv", "run", "-m", "server.main"]