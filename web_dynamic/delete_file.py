#!/usr/bin/python3
import sys
from models import fstorage
import json

response = input("Are you sure you want to clear this file? (yes/no): ")
if response == 'yes':
    with open('unikrib.json') as f:
        urls = json.load(f)
    for url in urls:
        fstorage.delete(url)
