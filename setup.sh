#!/bin/bash

python3 -m venv venv
source venv/Scripts/activate
pip3 install -r requirements.txt
clear

echo "Finished setup"