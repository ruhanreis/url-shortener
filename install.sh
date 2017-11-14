# Ask for the user password
# Script only works if sudo caches the password for a few minutes
sudo true

# Install docker
wget -qO- https://get.docker.com/ | sh

# Install docker-compose
sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.15.0/docker-compose-$(uname -s)-$(uname -m)"
sudo chmod +x /usr/local/bin/docker-compose

sudo docker-compose build --no-cache
