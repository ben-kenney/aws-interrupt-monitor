# Use Python 3.12 slim image
FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Set working directory
WORKDIR /app

# Copy script and install dependencies
ADD . /app
RUN uv sync --locked

# Run the script
CMD ["uv", "run", "src/main.py"]