echo "Running setup script."

if hash pip 2>/dev/null; then
    echo "pip is installed"
else
    echo "pip is missing"
    sudo apt-get install pip
fi

sudo pip install spotipy
sudo pip install numpy
