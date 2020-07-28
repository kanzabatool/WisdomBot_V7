#!/usr/bin/env bash
# Create a venv
source ../venv/bin/activate
pip install -r requirements.txt

FILE=../data/axillary/full_conceptnet_dicta

if [ -f "$FILE" ]; then
    echo "$FILE Already Exist"
else
    # if file not present download it from S3
    curl -wget https://wisdom-bot.s3-eu-west-1.amazonaws.com/full_conceptnet_dict ../data/axillary/full_conceptnet_dicta
fi
