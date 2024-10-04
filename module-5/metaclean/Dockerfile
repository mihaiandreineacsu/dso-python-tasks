# Use a base image with a lightweight Linux distribution
FROM ubuntu:latest

WORKDIR /metaclean

COPY ./app /metaclean

# Update package list and install dependencies, including Python
RUN apt-get update && apt-get install -y \
    exiftool \
    qpdf \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify the installation of exiftool, qpdf, and Python
RUN exiftool -ver && qpdf --version && python3 --version

# Set the default command to bash
CMD ["/bin/bash"]
