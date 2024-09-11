#!/usr/bin/python3

from models.engine.mysql_database import Storage
from models.engine.mongo_database import Database

# storage = Storage()
# storage = Database()
# storage.reload()

db = 'v1'  # This must always either be 'v1' or 'v2'

if db == 'v1':
    storage = Storage()
else:
    storage = Database()

if db == 'v1':
    from models.v1 import *
    # storage = Storage()
elif db == 'v2':
    from models.v2 import *
    # storage = Database()

storage.reload()