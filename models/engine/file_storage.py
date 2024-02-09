#!/usr/bin/python3
'''
FileStorage:
    is a class that serializes instances to a JSON file and
    deserializes JSON file to instances.
'''
import json
from os.path import isfile
from models.base_model import BaseModel


class FileStorage():
    '''
    FileStorage:
        is a class that serializes instances to a JSON file and
        deserializes JSON file to instances.

    Private Attributes:
        __file_path (str):  path to the JSON file.
        __objects (dict): Empty but will store all objects by <class name>.id.

    '''

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        '''Returns the dictionary __objects'''
        return self.__objects

    def new(self, obj):
        '''Sets in __objects the obj with key <obj class name>.id'''
        classname = obj.__class__.__name__
        obj_id = obj.id
        k = '{}.{}'.format(classname, obj_id)
        self.__objects[k] = obj

    def save(self):
        '''Serializes __objects to the JSON file (path: __file_path)'''
        with open(self.__file_path, 'w', encoding='utf-8') as storage:
            dictionary = {}
            for k, v in self.__objects.items():
                dictionary[k] = v.to_dict()

            json.dump(dictionary, storage)

    def reload(self):
        '''Deserializes the JSON file to __objects.

        Note: 
            only if the JSON file(__file_path exists; otherwise, do nothing.
            If the file doesn’t exist, no exception should be raised).
        '''
        if not isfile(self.__file_path):
            return

        with open(self.__file_path, 'r', encoding='utf-8') as file_obj:
            jsn = None

            try:
                jsn = json.loads(file_obj.read())
                self.serialize_loaded_json(jsn)
            except json.JSONDecodeError:
                pass

    def serialize_loaded_json(self, jsn):
        '''Serialize json loaded from file

        Args:
            jsn (str): json data
        '''
        classes = {'BaseModel', BaseModel}

        for v in jsn.values():
            classname = v['__class__']
            obj = getattr(classes, classname)(**v)
            self.new(obj)
