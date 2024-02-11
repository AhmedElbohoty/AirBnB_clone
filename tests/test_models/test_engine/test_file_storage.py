#!/usr/bin/python3
'''Unit tests for file storage module'''
import unittest
import json
import models
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    '''Unit tests for file storage module'''

    def test_file_storage_creation(self):
        '''Check file storage creation'''
        storage = FileStorage()
        self.assertEqual(type(storage), FileStorage)

    def test_file_storage_creation_args(self):
        '''Check file storage creation with args'''
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_file_storage_path_attribute(self):
        '''Check file storage private '__file_path' attribute'''
        storage = FileStorage()

        path_attr = '_FileStorage__file_path'

        self.assertIn(path_attr, dir(storage))
        self.assertIsInstance(getattr(storage, path_attr), str)
        self.assertEqual(getattr(storage, path_attr), 'file.json')

    def test_file_storage_objects_attribute(self):
        '''Check file storage private '__objects' attribute'''
        storage = FileStorage()

        objects_attr = '_FileStorage__objects'

        self.assertIn(objects_attr, dir(storage))
        self.assertIsInstance(getattr(storage, objects_attr), dict)

    def test_file_storage_classes_attribute(self):
        '''Check file storage private '__classes' attribute'''
        storage = FileStorage()

        classes_attr = '_FileStorage__classes'
        self.assertIn(classes_attr, dir(storage))
        self.assertIsInstance(getattr(storage, classes_attr), dict)


class TestFileStorageApp(unittest.TestCase):
    '''Unit tests for the main app storage'''

    def setUp(self):
        '''Create storage'''
        self.storage = FileStorage()
        self.storage.update_file_path('test_file.json')

    def tearDown(self):
        '''Reset storage'''
        self.storage.reset()

    def test_app_storage(self):
        '''Check if the main file storage is created'''
        self.assertEqual(type(self.storage), FileStorage)

    def test_all_empty(self):
        '''Test 'all' method'''
        storage = self.storage
        self.assertEqual(storage.all(), {})
        self.assertEqual(dict, type(storage.all()))

    def test_new_with_none(self):
        '''Test 'new' method '''
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_new(self):
        '''Test 'reload' method'''
        storage = self.storage
        bm = BaseModel()

        storage.new(bm)
        key = 'BaseModel.{}'.format(bm.id)
        self.assertIn(key, storage.all())
        self.assertEqual(str(storage.all()[key]), str(bm))

    def test_reload(self):
        '''Test 'reload' method'''
        storage = self.storage

        bm = BaseModel()
        storage.new(bm)
        storage.save()

        storage.reload()

        objects_attr = '_FileStorage__objects'
        objects = getattr(models.storage, objects_attr)

        self.assertIn('BaseModel.{}'.format(bm.id), objects)

    def test_save(self):
        ''''Tests the 'save' method'''
        storage = self.storage

        bm = BaseModel()
        storage.new(bm)
        storage.save()

        with open('test_file.json', 'r', encoding='UTF -8') as f:
            data = json.load(f)
            key = 'BaseModel.{}'.format(bm.id)
            self.assertIn(key, data)
            self.assertEqual(str(data[key]), str(bm.to_dict()))


if __name__ == '__main__':
    unittest.main()
