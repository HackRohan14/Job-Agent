#!/bin/bash

# Navigate to bot directory
cd job-bot

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run the bot
python main.py
