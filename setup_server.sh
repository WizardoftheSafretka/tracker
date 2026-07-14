#!/bin/bash

echo "Starting server setup for Tracker project..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create project directory
echo "Creating project directory..."
sudo mkdir -p /opt/tracker
sudo chown $USER:$USER /opt/tracker

# Install git
echo "Installing Git..."
sudo apt install git -y

# Install nginx (if needed)
echo "Installing Nginx..."
sudo apt install nginx -y

echo "Server setup complete!"
echo "Now copy .env.prod.example to /opt/tracker/.env and configure it"
echo "Then run: docker-compose -f docker-compose.prod.yml up -d"