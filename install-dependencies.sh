# install edge browser
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge-dev.list'
sudo rm microsoft.gpg

sudo apt update -y && sudo apt install microsoft-edge-stable -y

#install tor
sudo apt install tor -y
sudo service tor start

# install pip
sudo apt update -y && sudo apt install python3-pip -y
pip3 install --upgrade pip

# install requirements
cd ~/Scrapper
pip3 install -r requirements.txt
pip3 install --upgrade requests
