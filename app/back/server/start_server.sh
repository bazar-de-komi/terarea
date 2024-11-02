#!/bin/bash
. ./server_env/bin/activate
python3 ./src/ \
    --host 0.0.0.0 \
    --port 5000 \
    --debug
