# Use an official Ubuntu as a base image
FROM ubuntu:latest

# Set environment variables to non-interactive mode
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install OpenSSH server
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd

# Set up a user and password (e.g., 'docker' with password 'docker') without specifying UID
RUN useradd -rm -d /home/docker -s /bin/bash -g root -G sudo docker && \
    echo 'docker:docker' | chpasswd

# Allow password authentication
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose the SSH port
EXPOSE 22

# Start the SSH service
CMD ["/usr/sbin/sshd", "-D"]
