from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from passlib.apps import custom_app_context as pwd_context

import random
import string

from itsdangerous import(TimedJSONWebSignatureSerializer as
                         Serializer,
                         BadSignature,
                         SignatureExpired)

Base = declarative_base()

# You will use this secret key to create and verify your tokens
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for x in xrange(32))


class User(Base):
    '''
    User tabel contains the general information about the user.

    id            - Unique ID to differentiate every user
    username      - A username for the user
    email         - Email IDof the user
    password_hash - Saving the password in encrypted form
    '''

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    email = Column(String(250), nullable=False)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class Categories(Base):
    '''
    Categories tabel contains information about the a category.

    id      - Unique ID for every category
    name    - Name of the category
    user_id - A foriegn key associated with User table.
    '''

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class CategoryItem(Base):
    '''
    Categories tabel contains information about the a category.

    id          - Unique ID for each item
    name        - Name of the item
    description - A brief description about the item
    price       - Price of the item
    category_id - A foriegn key associated with Categories table
    user_id     - A foriegn key associated with User table
    '''

    __tablename__ = 'category_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Categories)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
        }

engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.create_all(engine)
