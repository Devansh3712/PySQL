@echo off
python -m venv venv
venv\Scripts\activate.bat & pip install -r requirements.txt & pip install --only-binary :all: mysqlclient