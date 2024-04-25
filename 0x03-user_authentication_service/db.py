#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User



class DB:
    """ DB class """
    def __init__(self) -> None:
        """ Initialize a new DB instance """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds a user to the table """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user
    
    def find_user_by(self, **kwargs) -> User:
        """ Finds a user in the table """
        #create a query to find users based on the provided filters
        query = self._session.query(User)
        for key, value in kwargs.items():
            #check if the key exists as an attr in the user class
            if key in User.__dict__:
                query = query.filter_by(**{key: value})
            else:
                raise InvalidRequestError
        #Execute the query and retrieve the first matching user
        result = query.first()
        if result is None:
            raise NoResultFound
        return result
   
    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates the user """
        try:
            #find the user by user_id
            user = self.find_user_by(id=user_id)
            #Update the user's attrs
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            #Commit changes to the db
            self._session.commit()
        except NoResultFound:
            raise ValueError

