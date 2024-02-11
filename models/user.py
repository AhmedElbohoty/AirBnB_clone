#!/usr/bin/python3
'''
User:
    - It is a class that defines all common attributes/methods for users.
    - It inherits from BaseModel
'''
from models.base_model import BaseModel


class User(BaseModel):
    '''User:
    - It is a class that defines all common attributes/methods for users.
    - It inherits from BaseModel

    Attributes:
        email (str): user's email.
        password (str): user's password.
        first_name (str): user's first name.
        last_name (str): user's last name.
    '''

    first_name = ''
    last_name = ''
    email = ''
    password = ''
