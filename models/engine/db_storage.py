#!/usr/bin/python3
"""database storage engine"""
from os import getenv
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import text
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST', default='localhost')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        # self.__engine = create_engine({
        #     'engine': 'mysql+mysqldb',
        #     'user': HBNB_MYSQL_USER,
        #     'password': HBNB_MYSQL_PWD,
        #     'host': HBNB_MYSQL_HOST,
        #     'database': HBNB_MYSQL_DB,
        #     'pool_pre_ping': True
        # })
        self.__engine = create_engine(
            'mysql+mysqldb://' +
            HBNB_MYSQL_USER +
            ':' +
            HBNB_MYSQL_PWD +
            '@' +
            HBNB_MYSQL_HOST +
            '/' +
            HBNB_MYSQL_DB)

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        classes = [User, State, City, Amenity, Place, Review]
        objects = {}

        if cls is not None:
            if cls in classes:
                return {obj.__class__.__name__ + '.' + obj.id:
                        obj for obj in self.__session.query(cls).all()}
            else:
                return {}
        else:
            for c in classes:
                for obj in self.__session.query(text(c.__name__)).all():
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
            return objects

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()