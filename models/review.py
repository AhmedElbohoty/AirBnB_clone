#!/usr/bin/python3
'''
Review
'''
from models.base_model import BaseModel


class Review(BaseModel):
    '''Review

    Attributes:
        name (str): review name.
        user_id (str): The User.id.
        place_id (str): The Place.id.
    '''

    text = ''
    user_id = ''
    place_id = ''
