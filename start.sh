#!/bin/bash

source .env

virtualenv flask
flask/bin/pip install -r requirements.txt
flask/bin/python data_manager/app.py
