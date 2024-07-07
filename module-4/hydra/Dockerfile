# Use an official Python runtime as a parent image
FROM python:3.9-slim

ARG PASSWORD="changeme"
ARG PORT=22

ENV PASSWORD=${PASSWORD} \
    PORT=${PORT}

# Install OpenSSH server
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd

# Set the root password (replace '$PASSWORD' with a secure password)
RUN echo "root:${PASSWORD}" | chpasswd

# Allow root login and password authentication
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i "s/#Port 22/Port ${PORT}/" /etc/ssh/sshd_config

# Expose SSH port
EXPOSE ${PORT}

# Start the SSH service
CMD ["/usr/sbin/sshd", "-D"]
