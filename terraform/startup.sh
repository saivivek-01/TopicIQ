#!/bin/bash

# Update system
apt-get update -y
apt-get upgrade -y

# Install Docker
apt install -y docker.io
systemctl enable docker
systemctl start docker

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
-o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Set up root user to use Docker without sudo
usermod -aG docker root

# Install Git and unzip (for code deployment)
apt-get install -y git unzip

# Create app folder (optional)
mkdir -p /root/TopicIQ