#!/usr/bin/python3

import json
filepath = 'backup.json'

def backup():
    from models.v1 import storage as mysql_storage

    all_objs = []
    for obj in mysql_storage.all().values():
        if obj.__class__ == 'Code' or obj.__class__ == 'UserSession':
            continue
        all_objs.append(obj)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_objs, f)


def restore():
    from models import storage as mongo_storage

    with open(filepath) as f:
        all_objs = json.load(f)

    for obj in all_objs:
        model = mongo_storage.reload(obj['__class__'])
        model.save()
    