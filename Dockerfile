FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    openjdk-11-jdk-headless \
    git build-essential libssl-dev libffi-dev \
    libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev \
    autoconf libtool pkg-config \
    ant unzip wget && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --upgrade pip && \
    pip install buildozer Cython==0.29.33 virtualenv

# Install Kivy and dependencies
RUN pip install kivy Pillow

# Set working directory
WORKDIR /project

# Entrypoint for buildozer
ENTRYPOINT ["buildozer"]
CMD ["android", "release"]
