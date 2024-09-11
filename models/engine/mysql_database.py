#!/usr/bin/env python3
"""
Database engine
"""

from os import getenv
from models.v1.code import Code
from models.v1.user import User
from models.v1.house import House
from models.v1.street import Street
from models.v1.review import Review
from models.v1.report import Report
from models.v1.school import School
from models.v1.service import Service
from models.v1.product import Product
from models.v1.base_model import Base
from models.v1.category import Category
from models.v1.transaction import Transaction
from models.v1.environment import Environment
from models.v1.user_session import UserSession
from models.v1.notification import Notification
from models.v1.service_category import ServiceCategory
from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import sessionmaker, scoped_session


class Storage:
    """
    storage of class instances
    """
    classes = {"Code": Code, "User": User, "Product": Product,
            "House": House, "Environment": Environment, "Street": Street,
            "Review": Review, "Category": Category, "Service": Service,
            "ServiceCategory": ServiceCategory, "Report": Report,
            'UserSession': UserSession, 'Notification': Notification,
            "Transaction": Transaction, "School": School}

    __engine = None
    __session = None

    def __init__(self):
        """
        initialize the engine
        """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}?charset=utf8mb4'.format(
                getenv('DB_USER'),
                getenv('DB_PASSWD'),
                getenv('HOST'),
                getenv('DB_NAME')
            ))

    def all(self, cls=None):
        """
        returns all objects
        """
        obj_dict = {}
        if cls is not None:
            try:
                a_query = self.__session.query(cls).all()
            except:
                cs = self.classes[cls]
                a_query = self.__session.query(cs).all()
            for obj in a_query:
                if cls == 'Code' or cls == 'UserSession':
                    search_key = '{}.{}'.format(obj.__class__.__name__, obj.user_id)
                else:
                    search_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                obj_dict[search_key] = obj
        else:
            for key, cls in self.classes.items():
                a_query = self.__session.query(cls)
                for obj in a_query:
                    obj_ref = '{}.{}'.format(type(obj).__name__, obj.id)
                    obj_dict[obj_ref] = obj

        return obj_dict

    def new(self, obj):
        """
        add object to db
        """
        self.__session.add(obj)

    def save(self):
        """
        commits changes to db session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes obj from db session if obj != None
        """
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """
        creates tables in db and session from engine
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """
        calls remove() on session attribute
        """
        self.__session.remove()

    def get(self, cls, id):
        """
        gets one object based on the class and id
        """
        if cls and id:
            if isinstance(cls, str):
                cls = self.classes[cls]
            if cls == Code or cls == UserSession:
                obj = self.search(cls, user_id=id)
            else:
                obj = self.search(cls, id=id)
            if obj is None or obj == []:
                return None
            return obj[0]
        return None

    def search(self, cls, **kwargs):
        """This searches the database based on the keyword
        arg"""
        if not cls:
            return None
        if isinstance(cls, str):
            if cls not in self.classes:
                return None
            cls = self.classes[cls]


        obj = self.__session.query(cls).filter_by(**kwargs).all()
        if obj is None or obj == []:
            return []
        return obj

    def count(self, cls=None, key=None):
        """
        returns count of all objects
        """
        if key is not None and key == "rooms_available":
            return (self.__session.query(func.sum(cls.rooms_available)).scalar())
        return (len(self.all(cls)))

    def paginate_query(self, cls, page_num, page_size, **kwargs):
        """This returns a regulated amount of results
        """
        if not kwargs:
            try:
                offset = (int(page_num) - 1) * int(page_size)
                results = self.__session.query(cls).offset(offset).limit(page_size).all()
            except Exception as e:
                print(e)
                results = []
            return results
        else:
            try:
                offset = (int(page_num) - 1) * int(page_size)
                results = self.__session.query(cls).filter_by(**kwargs).offset(offset).limit(page_size).all()
            except Exception as e:
                print(e)
                results = []
            return results
        
    def listFilter(self, cls, **kwargs):
        """This filters a table based on a list of items"""
        if not cls:
            return None
        if isinstance(cls, str):
            if cls not in self.classes:
                return None
            cls = self.classes[cls]

        results = []
        
        for key, val in kwargs.items():
            if key in ("street_id", "max_price", "min_price"):
                if key == 'street_id' and isinstance(val, list):
                    results.append(cls.street_id.in_(val))
                if key == "max_price":
                    results.append(cls.price <= val)
                if key == "min_price":
                    results.append(cls.price >= val)
            else:
                results.append(cls.__dict__[key] == val)

        try:
            obj = self.__session.query(cls).filter(and_(*results)).all()
        except Exception as e:
            print(e)
            obj = []
        return obj

    def sort_limit(self, cls, limit):
        """This sorts all the objects of class cls by the key "key" and returns a 
        limited amount of objs"""
        objs = self.__session.query(cls).order_by(cls.no_clicks.desc()).limit(limit)
        return objs
