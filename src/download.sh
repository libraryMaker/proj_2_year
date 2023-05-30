sudo apt update
sudo apt full-upgrade
sudo apt install python3-pip
sudo pip3 install --upgrade setuptools
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
sudo pip3 install adafruit-circuitpython-dht
sudo pip install mh_z19
sudo python -m mh_z19
sudo apt-get install libgpiod2
sudo adduser pi i2c
sudo apt-get install i2c-tools python-pip
i2cdetect -y 1
sudo pip install RPi.bme280
sudo apt install mariadb-server
sudo mysql_secure_installation
sudo pip install mysql-connector-python
sudo mysql -u root -p < mysql_script.sql
sudo reboot