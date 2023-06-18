#!/bin/bash
python3 -m venv .gw_env
source .gw_env/bin/activate
pip install -r requirements.txt
docker-compose up -d
