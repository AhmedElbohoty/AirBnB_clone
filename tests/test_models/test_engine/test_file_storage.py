#!/usr/bin/python3
'''Unit tests for file storage module'''
import unittest
import models
from models.engine.file_storage import FileStorage


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

    @classmethod
    def setUpClass(cls):
        '''Update file path for test'''
        models.storage.update_file_path('test_file.json')

    @classmethod
    def tearDownClass(cls):
        '''Update file path for app'''
        models.storage.update_file_path('file.json')

    def test_app_storage(self):
        '''Check if the main file storage is created'''
        self.assertEqual(type(models.storage), FileStorage)

    def test_all(self):
        '''Test 'all' method'''
        self.assertEqual(dict, type(models.storage.all()))

    def test_new_with_none(self):
        '''Test 'new' method '''
        with self.assertRaises(AttributeError):
            models.storage.new(None)


if __name__ == '__main__':
    unittest.main()
