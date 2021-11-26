#!/bin/bash

sudo apt install python3-dev
sudo apt install libmysqlclient-dev
pip3 install mysqlclient
pip3 install -r requirements.txt
python3 setup.py install
clear
echo "PySQL installation complete"
