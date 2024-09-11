#!/usr/bin/python3

import pymongo
from os import getenv
from datetime import datetime

classes = {"codes": "Code", "users": "User", "products": "Product",
            "houses": "House", "environments": "Environment", "streets": "Street",
            "reviews": "Review", "categories": "Category", "services": "Service",
            "service_categories": "ServiceCategory", "reports": "Report",
            'usersession': "UserSession", 'notifications': "Notification",
            "transactions": "Transaction"}


class Database:
    all_objs = {}

    def __init__(self):
        db_name = getenv('DB_NAME', 'unikrib_db')
        url = getenv("HOST", 'localhost')
        # port = getenv("PORT", )
        try:
            self.client = pymongo.MongoClient(url)
            self.db = self.client[db_name]
        except Exception as e:
            print("Unable to connect to mongo server:", e)

    def all(self, cls=None):
        if cls and cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls and cls not in classes:
            print(cls)
            cls = cls.__tablename__

        objs = {}

        if not cls:
            for cs in classes:
                documents = self.db[cs].find()
                for doc in documents:
                    if doc['__class__'] == 'Code' or doc['__class__'] == 'UserSession':
                        key = "{}.{}".format(doc['__class__'], doc['user_id'])
                    else:
                        key = "{}.{}".format(doc['__class__'], doc['id'])
                    model = self.reload(doc['__class__'], **doc)
                    objs[key] = model
        else:
            documents = self.db[cls].find()
            for doc in documents:
                if cls == 'codes':
                    key = "{}.{}".format(doc['__class__'], doc['user_id'])
                else:
                    key = "{}.{}".format(doc['__class__'], doc['id'])
                model = self.reload(doc['__class__'], **doc)
                objs[key] = model
        return objs

    def save(self, model):
        """
        Save a new document in the specified collection.
        Args:
            model (class): The model class representing the collection.
        """
        if model.__tablename__ == 'codes' or model.__tablename__ == 'usersession':
            objs = self.db[model.__tablename__].find({ "id": model.user_id })
        else:
            objs = self.db[model.__tablename__].find({ "id": model.id })
        existing_docs = []
        for obj in objs:
            existing_docs.append(obj)
        if existing_docs:
            # if the document instance already exist, update it
            query = {'id': model.id}
            new_attrs = {"$set": model.to_dict()}
            self.db[model.__tablename__].update_one(query, new_attrs)
            print("Document updated successfully")
        else:
            # If the document instance does not exist yet, create a new document
            try:
                obj_dict = model.to_dict()
                self.db[model.__tablename__].insert_one(obj_dict)
                print('Document saved successfully.')
            except pymongo.errors.PyMongoError as e:
                print(f'Error saving document: {e}')
            except Exception as e:
                print(f"Error encountered: {e}") 

    def delete(self, model):
        """
        Remove a document from the specified collection based on a query.
        Args:
            model (class): The instance representing the document.
        """
        try:
            dic = model.to_dict()
            result = self.db[dic.__class__].delete_one({'id': model['id']})
            print(f'{result.deleted_count} document(s) deleted successfully.')
        except pymongo.errors.PyMongoError as e:
            print(f'Error deleting document(s): {e}')

    def close(self):
        self.client.close()

    def reload(self, cls, **values):
        """This recreates a class object from the given values"""
        from models.v1.user import User
        from models.v1.code import Code
        from models.v1.house import House
        from models.v1.product import Product
        from models.v1.service import Service
        from models.v1.street import Street
        from models.v1.review import Review
        from models.v1.report import Report
        from models.v1.category import Category
        from models.v1.transaction import Transaction
        from models.v1.notification import Notification
        from models.v1.environment import Environment
        from models.v1.user_session import UserSession
        from models.v1.service_category import ServiceCategory

        del(values['_id'])

        try:
            if cls == "users" or cls == "User":
                model = User(**values)
            if cls == 'codes' or cls == 'Code':
                model = Code(**values)
            if cls == 'houses' or cls == "House":
                model = House(**values)
            if cls == 'products' or cls == 'Product':
                model = Product(**values)
            if cls == 'services' or cls == 'Service':
                model = Service(**values)
            if cls == 'streets' or cls == "Street":
                model = Street(**values)
            if cls == 'reviews' or cls == "Review":
                model = Review(**values)
            if cls == 'reports' or cls == "Report":
                model = Report(**values)
            if cls == 'categories' or cls == 'Category':
                model = Category(**values)
            if cls == 'environments' or cls == 'Environment':
                model = Environment(**values)
            if cls == 'notifications' or cls == 'Notification':
                model = Notification(**values)
            if cls == 'transactions' or cls == "Transaction":
                model = Transaction(**values)
            if cls == 'usersession' or cls == 'UserSession':
                model = UserSession(**values)
            if cls == 'service_category' or cls == 'ServiceCategory':
                model = ServiceCategory(**values)
        except ValueError as e:
            print(e)
            return None

        try:
            if hasattr(model, "created_at") and isinstance(model.created_at, str):
                created_at = datetime.strptime(model.created_at, "%Y-%m-%dT%H:%M:%S")
                model.created_at = created_at.strftime("%d-%m-%Y %H:%M")
            if hasattr(model, "updated_at") and isinstance(model.updated_at, str):
                updated_at = datetime.strptime(model.updated_at, "%Y-%m-%dT%H:%M:%S.%f")
                model.updated_at = updated_at.strftime("%d-%m-%Y %H:%M")
        except Exception as e:
            print("Error at reload", e)
            pass
        return model
        
    def get(self, cls, id):
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            cls = cls.__tablename__

        try:
            if cls == 'codes' or cls == 'usersession':
                doc = self.db['cls'].find_one({ 'user_id': id })
            else:
                doc = self.db[cls].find_one({ 'id': id })
            if doc:
                model = self.reload(doc['__class__'], **doc)
                return model
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def search(self, cls, **kwargs):
        """This filters the storage for objects matching kwargs
        Args:
            cls (str): The class to search for the documents
            kwargs (dict): filter parameters
        Return:
            A list of documents matching the description
        """
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            cls = cls.__tablename__

        result = []
        docs = self.db[cls].find( kwargs )
        for doc in docs:
            model = self.reload(doc['__class__'], **doc)
            result.append(model)
        return result
    
    def count(self, cls, key=None):
        """This counts the number of documents in a cls,
            If key is provided, it sums all the values of that key in the collection
        Args:
            cls (str): the class name or collection
            key (str): [optional] key containing the field to count
        Return:
            int: count of found documents
        """
        if cls not in classes:
            for k, v in classes.items():
                if v == cls:
                    cls = k
                    break
        if cls not in classes:
            cls = cls.__tablename__

        if key:
            try:
                result = self.db[cls].aggregate([
                    {"$group": {"_id": None, "sum": {"$sum": f"${key}"}}}
                ])
                sum_value = 0
                for doc in result:
                    sum_value = doc['sum']
                return sum_value
            except Exception as e:
                print(e)
        return self.db[cls].count()

    def paginate_query(self, cls, pgnum, pgsize, **kwargs):
        """This handles pagination by returning limited data
        Args:
            cls (str): the collection name or class
            pgnum (int): the page number
            pgsize (int): the items to return per page
        Return:
            a list of requested items"""
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            cls = cls.__tablename__
        pgnum = int(pgnum)
        pgsize = int(pgsize)

        if not kwargs:
            result = []
            try:
                offset = (int(pgnum) - 1) * int(pgsize)
                documents = self.db[cls].find().skip(offset).limit(pgsize)
                for document in documents:
                    model = self.reload(document['__class__'], **document)
                    result.append(model)
                return result
            except Exception as e:
                print(e)
                return result
        else:
            result = []
            try:
                offset = (int(pgnum) - 1) * int(pgsize)
                documents = self.db[cls].find( kwargs ).skip(offset).limit(pgsize)
                for document in documents:
                    model = self.reload(document['__class__'], **document)
                    result.append(model)
                return result
            except Exception as e:
                print(e)
                return result

    def search_paginate(self, cls, pgnum, pgsize, **kwargs):
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            cls = cls.__tablename__


        try:
            offset = (int(pgnum) - 1) * int(pgsize)
            result = self.db[cls].find( kwargs ).skip(offset).limit(pgsize)
            return result
        except Exception as e:
            print(e)
            return []
        
    def listFilter(self, cls, **kwargs):
        """
        Filter the collection based on a dictionary of filter parameters.
        Args:
            cls (class): The model class representing the collection.
            kwargs (dict): A dictionary of filter parameters where values can be lists.
        Returns:
            list: A list of filtered documents.
        """
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            cls = cls.__tablename__


        result = []
        try:
            query = {}
            for key, values in kwargs.items():
                if key == 'max_price' and 'min_price' in kwargs.items():
                    query['price'] = {"$gte": kwargs['min_price'], "$lte": values}
                elif key == 'min_price' and 'max_price' in kwargs:
                    query['price'] = {"$gte": values, "$lte": kwargs['max_price']}
                elif isinstance(values, list):
                    query[key] = {"$in": values}
                elif key != 'max_price' and key != 'min_price':
                    query[key] = values
            # query = {key: {"$in": values} if isinstance(values, list) else values
            #          for key, values in kwargs.items()}
            documents = self.db[cls].find(query)
            for document in documents:
                model = self.reload(document['__class__'], **document)
                result.append(model)
            return result
        except pymongo.errors.PyMongoError as e:
            print(f'Error performing list filter: {e}')
            return []

    def sort_limit(self, cls, limit):
        if cls not in classes:
            for key, val in classes.items():
                if val == cls:
                    cls = key
                    break
        if cls not in classes:
            cls = cls.__tablename__


        objs = self.db[cls].find().sort("no_clicks", -1).limit(limit)
        result = []
        for obj in objs:
            model = self.reload(obj['__class__'], **obj)
            result.append(model)
        return result
