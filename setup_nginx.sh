#!/bin/bash

# Install Nginx
sudo apt-get install -y nginx

# Create Nginx configuration
cat <<EOL | sudo tee /etc/nginx/sites-available/flask-app
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL

# Enable the new configuration
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx to apply changes
sudo systemctl restart nginx
