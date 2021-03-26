#!/bin/bash

python3 -m venv venv
source venv/bin/activate
sudo apt install python3-dev
sudo apt install libmysqlclient-dev
pip3 install mysqlclient
pip3 install -r requirements.txt
clear

echo "Finished PySQL setup"
