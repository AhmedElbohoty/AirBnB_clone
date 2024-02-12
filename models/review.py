#!/usr/bin/python3
'''
Review
'''
from models.base_model import BaseModel


class Review(BaseModel):
    '''Review

    Attributes:
        text (str): review text.
        user_id (str): The User.id.
        place_id (str): The Place.id.
    '''

    text = ''
    user_id = ''
    place_id = ''
