#!/usr/bin/python3
'''
City
'''
from models.base_model import BaseModel


class City(BaseModel):
    '''City:

    Attributes:
        name (str): city.
        state_id (str): The State id.
    '''

    name = ''
    state_id = ''
