#!/bin/bash

# Navigate to bot directory
cd job-bot

# Upgrade pip and install dependencies
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

# Run the bot
python3 job-bot/main.py
