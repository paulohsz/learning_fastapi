# Use Debian Bookworm as base image
FROM debian:bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and install Python 3.13.7 (latest stable version)
RUN wget https://www.python.org/ftp/python/3.13.7/Python-3.13.7.tgz \
    && tar xzf Python-3.13.7.tgz \
    && cd Python-3.13.7 \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.13.7 Python-3.13.7.tgz

# Set Python 3.13 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.13 1 \
    && update-alternatives --set python3 /usr/local/bin/python3.13

# Install pip
RUN wget https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py

# Install pipx and poetry
RUN python3 -m pip install --no-cache-dir pipx && \
    python3 -m pipx ensurepath || true && \
    # Ensure local bin is in PATH for root
    mkdir -p /root/.local/bin && \
    echo 'export PATH="/root/.local/bin:$PATH"' >> /etc/profile.d/local_bin.sh

# Set working directory
WORKDIR /app

# Optionally install development dependencies during image build
ARG INSTALL_DEV=false
ENV INSTALL_DEV=${INSTALL_DEV}

# Copy requirements and install Python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt \
    && if [ "${INSTALL_DEV}" = "true" ]; then pip3 install --no-cache-dir -r requirements-dev.txt; fi

# Copy the application code
COPY . .

# Expose port 8070
EXPOSE 8070

# Create an entrypoint script to run the application with proper signal handling
# Using an entrypoint script ensures signals are forwarded correctly and uvicorn runs as PID 1
RUN printf '%s\n' "#!/bin/sh" "set -e" "if [ \"\$INSTALL_DEV\" = \"true\" ]; then" \
    "  exec uvicorn app.main:app --host 0.0.0.0 --port 8070 --reload" \
    "else" \
    "  exec uvicorn app.main:app --host 0.0.0.0 --port 8070" \
    "fi" > /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]