#!/usr/bin/python3
'''
BaseModel:
    is a class that defines all common attributes/methods for other classes.
'''

from uuid import uuid4
from datetime import datetime


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
        if len(kwargs) == 0:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            return

        dates_attrs = ['created_at', 'updated_at']
        for k, v in kwargs.items():
            if k == '__class__':
                continue

            if k in dates_attrs:
                v = datetime.fromisoformat(v)

            setattr(self, k, v)

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

    def __str__(self):
        '''Return the representation of Instance.'''
        instance_id = self.id
        classname = self.__class__.__name__
        instance_dict = self.__dict__
        return '[{}] ({}) {}'.format(classname, instance_id, instance_dict)


# my_model = BaseModel()
# my_model.name = "My_First_Model"
# my_model.my_number = 89
# print(my_model.id)
# print(my_model)
# print(type(my_model.created_at))
# print()
# print()
# print()
# my_model_json = my_model.to_dict()
# print(my_model_json)
# print("JSON of my_model:")
# for key in my_model_json.keys():
#     print("\t{}: ({}) - {}".format(key,
#           type(my_model_json[key]), my_model_json[key]))

# print()
# print()
# print()
# my_new_model = BaseModel(**my_model_json)
# print(my_new_model.id)
# print(my_new_model)
# print(type(my_new_model.created_at))

# print()
# print()
# print()
# print(my_model is my_new_model)
