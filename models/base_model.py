#!/usr/bin/python3
'''
BaseModel:
    is a class that defines all common attributes/methods for other classes.
'''

from uuid import uuid4
from datetime import datetime
import models


class BaseModel():
    '''Base class that defines all common attributes/methods for other classes

    Attributes:
        id (str): unique id.
        created_at (datetime): The datetime when an instance is created.
        updated_at (datetime): The datetime when an instance is created
                               and it will be updated with every changes.
    '''

    def __init__(self, **kwargs):
        '''Initialize the instance

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        '''
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if len(kwargs) != 0:
            dates_attrs = ['created_at', 'updated_at']
            for k, v in kwargs.items():
                if k == '__class__':
                    continue

                if k in dates_attrs:
                    v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')

                setattr(self, k, v)

        if len(kwargs) == 0:
            models.storage.new(self)

    def to_dict(self):
        '''Returns a dictionary representation of a instance.

        Returns:
            dict: instance attributes.
        '''
        dictionary = {**self.__dict__}
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        return dictionary

    def save(self):
        '''Updates the public instance attribute updated_at'''
        self.updated_at = datetime.now()

        models.storage.save()

    def __str__(self):
        '''Return the representation of Instance.'''
        instance_id = self.id
        classname = self.__class__.__name__
        instance_dict = self.__dict__
        return '[{}] ({}) {}'.format(classname, instance_id, instance_dict)
