#!/bin/bash

# Run setup environment script
./setup_env.sh

# Re-login to apply Docker group changes
exec sg docker newgrp `id -gn`

# Run build and deploy Docker script
./deploy_docker.sh

# Run Nginx setup script
./setup_nginx.sh
