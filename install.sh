# Ask for the user password
# Script only works if sudo caches the password for a few minutes
sudo true

# Install docker
if which docker > /dev/null ; then
    echo "Docker is already installed"
 else
 	wget -qO- https://get.docker.com/ | sh	
fi

# Install docker-compose
if which docker-compose > /dev/null ; then
	echo "Docker Compose is already installed"
else
	sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.15.0/docker-compose-$(uname -s)-$(uname -m)"
	sudo chmod +x /usr/local/bin/docker-compose
fi

sudo docker-compose build --no-cache
