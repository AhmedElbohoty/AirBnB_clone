#!/usr/bin/python3
'''Unit tests for file storage module'''
import unittest
import json
import models
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


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

    def test_init_no_args(self):
        '''Create file storage with no arguments'''
        with self.assertRaises(TypeError):
            FileStorage.__init__()

    def test_init_extra_arg(self):
        '''Tests __init__ with many arguments'''
        with self.assertRaises(TypeError):
            FileStorage('arg')


class TestFileStorageAll(unittest.TestCase):
    '''Unit tests for 'all' method'''

    def setUp(self):
        '''Create storage'''
        self.storage = models.storage
        self.storage.update_file_path('test_file.json')

    def tearDown(self):
        '''Reset storage'''
        self.storage.reset()

    def test_all_empty(self):
        '''Test 'all' method'''
        storage = self.storage
        self.assertEqual(storage.all(), {})
        self.assertEqual(dict, type(storage.all()))

    def test_all_non_empty(self):
        '''Test the all 'method' non-empty'''
        storage = self.storage

        bm = BaseModel()
        storage.new(bm)

        key = 'BaseModel.{}'.format(bm.id)
        self.assertEqual(storage.all(), {key: bm})

    def test_all_base_model(self):
        '''Tests 'all' method for BaseModel'''
        storage = self.storage

        bm = BaseModel()
        storage.new(bm)
        key = 'BaseModel.{}'.format(bm.id)

        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], bm)

    def test_all_user(self):
        '''Tests 'all' method for User'''
        storage = self.storage

        user = User()
        storage.new(user)
        key = 'User.{}'.format(user.id)

        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], user)

    def test_all_state(self):
        '''Tests 'all' method for State'''
        storage = self.storage

        state = State()
        storage.new(state)
        key = 'State.{}'.format(state.id)

        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], state)

    def test_all_city(self):
        '''Tests 'all' method for City'''
        storage = self.storage

        city = City()
        storage.new(city)
        key = 'City.{}'.format(city.id)

        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], city)

    def test_all_amenity(self):
        '''Tests 'all' method for Amenity'''
        storage = self.storage

        amenity = Amenity()
        storage.new(amenity)
        key = 'Amenity.{}'.format(amenity.id)

        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], amenity)

    def test_all_place(self):
        '''Tests 'all' method for Place'''
        storage = self.storage

        place = Place()
        storage.new(place)
        key = 'Place.{}'.format(place.id)

        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], place)

    def test_all_review(self):
        '''Tests 'all' method for Review'''
        storage = self.storage

        review = Review()
        storage.new(review)
        key = 'Review.{}'.format(review.id)

        self.assertTrue(key in storage.all())
        self.assertEqual(storage.all()[key], review)

    def test_all_no_args(self):
        '''Tests 'all' with no arguments'''
        with self.assertRaises(TypeError):
            FileStorage.all()

    def test_all_excess_args(self):
        '''Tests 'all' with extra argument'''
        with self.assertRaises(TypeError):
            FileStorage.all(self, 'arg')


class TestFileStorageNew(unittest.TestCase):
    '''Unit tests for the 'new' method'''

    def setUp(self):
        '''Create storage'''
        self.storage = models.storage
        self.storage.update_file_path('test_file.json')

    def tearDown(self):
        '''Reset storage'''
        self.storage.reset()

    def test_new_base_model(self):
        '''Test 'new' method'''
        storage = self.storage
        bm = BaseModel()

        storage.new(bm)
        key = 'BaseModel.{}'.format(bm.id)
        self.assertIn(key, storage.all())
        self.assertEqual(str(storage.all()[key]), str(bm))

    def test_new_user(self):
        '''Test 'new' method for User'''
        storage = self.storage
        user = User()

        storage.new(user)
        key = 'User.{}'.format(user.id)
        self.assertIn(key, storage.all())
        self.assertEqual(str(storage.all()[key]), str(user))

    def test_new_amenity(self):
        '''Test 'new' method for Amenity'''
        storage = self.storage
        amenity = Amenity()

        storage.new(amenity)
        key = 'Amenity.{}'.format(amenity.id)
        self.assertIn(key, storage.all())
        self.assertEqual(str(storage.all()[key]), str(amenity))

    def test_new_city(self):
        '''Test 'new' method for City'''
        storage = self.storage
        city = City()

        storage.new(city)
        key = 'City.{}'.format(city.id)
        self.assertIn(key, storage.all())
        self.assertEqual(str(storage.all()[key]), str(city))

    def test_new_place(self):
        '''Test 'new' method for Place'''
        storage = self.storage
        place = Place()

        storage.new(place)
        key = 'Place.{}'.format(place.id)
        self.assertIn(key, storage.all())
        self.assertEqual(str(storage.all()[key]), str(place))

    def test_new_review(self):
        '''Test 'new' method for Review'''
        storage = self.storage
        review = Review()

        storage.new(review)
        key = 'Review.{}'.format(review.id)
        self.assertIn(key, storage.all())
        self.assertEqual(str(storage.all()[key]), str(review))

    def test_new_state(self):
        '''Test 'new' method for State'''
        storage = self.storage
        state = State()

        storage.new(state)
        key = 'State.{}'.format(state.id)
        self.assertIn(key, storage.all())
        self.assertEqual(str(storage.all()[key]), str(state))


class TestFileStorageApp(unittest.TestCase):
    '''Unit tests for the main app storage'''

    def setUp(self):
        '''Create storage'''
        self.storage = models.storage
        self.storage.update_file_path('test_file.json')

    def tearDown(self):
        '''Reset storage'''
        self.storage.reset()

    def test_app_storage(self):
        '''Check if the main file storage is created'''
        self.assertEqual(type(self.storage), FileStorage)

    def test_new_with_none(self):
        '''Test 'new' method '''
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_reload_class(self):
        '''Test 'reload' method'''
        FileStorage().reload()

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
