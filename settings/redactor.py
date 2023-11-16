#!/usr/bin/python3
"""This filters data and redacts some fields"""
import re

class Redacter():
    """class definition"""
    def __init__(self, field):
        self.field = field


    def filter_datum(self, separator, data):
        """Args:
            fields: a list of keys to redact
            separator: the delimiter in the data
            data: The data to filter
        """
        for key, val in data.items():
            if key in self.field:
                data[key] = "*" * len(val)
                #new_item = re.sub(key + ":" + val,
                                 #key + ":" + "***", item)
                #data = re.sub(item, new_item, data)
        return data