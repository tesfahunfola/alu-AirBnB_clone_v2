#!/usr/bin/python3
"""DBStorage"""
from sqlalchemy import create_engine
import os
from models.base_model import Base
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity
from models.city import City
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Database Storage using SQLAlchemy ORM"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize Instance"""

        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        # To test locally
        # connection_url = 'mysql+pymysql://{}:{}@{}:3306/{}'.format(
        #     user, password, host, database)
        connection_url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
            user, password, host, database)

        self.__engine = create_engine(connection_url, pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return all table(s) depending on cls value"""

        classes = {
            'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        obj_dict = {}

        if cls is None:
            for cls in classes:
                class_objects = self.__session.query(classes[cls]).all()
                for obj in class_objects:
                    key = obj.__class__.__name__ + "." + obj.id
                    obj_dict[key] = obj

        if cls in classes:
            class_objects = self.__session.query(classes[cls]).all()
            for obj in class_objects:
                key = obj.__class__.__name__ + "." + obj.id
                obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """Adds obj to the database"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from current database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload Session"""

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
