FROM python:3.10

# Install Docker and Node.js
RUN apt-get update && apt-get install -y \
    docker.io \
    curl \
    ca-certificates \
    gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Update npm to latest version and verify installation
RUN npm install -g npm@latest \
    && node --version && npm --version && npx --version

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy your project
COPY . /app
WORKDIR /app

# Install dependencies
RUN uv sync

# Expose any ports your app needs
EXPOSE 10000

CMD ["uv", "run", "server.py"]