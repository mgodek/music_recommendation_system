echo "Running setup script."

if [ ! -f "10000.txt" ];
then
        wget https://www.dropbox.com/s/4ga0gq2khsdik5j/10000.txt.gz
	wget https://www.dropbox.com/s/22uw0145rntk03f/song_data.csv.gz
	wget https://www.dropbox.com/s/5k90w842loqc17t/user_favorites_translation.txt.gz
	wget https://www.dropbox.com/s/02zxqrqpb8lx7xf/user_favorites.txt.gz
	FILES=("10000.txt.gz" "song_data.csv.gz" "user_favorites.txt.gz" "user_favorites_translation.txt.gz")
	for filename in "${FILES[@]}"
	do
		echo "$filename"
        	gunzip "$filename"
	done
fi

if hash pip 2>/dev/null; then
    echo "pip is installed"
else
    echo "pip is missing"
    sudo apt-get install pip
fi

sudo pip install spotipy
sudo pip install numpy
