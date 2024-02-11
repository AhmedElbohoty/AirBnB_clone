#!/usr/bin/python3
'''Unit tests for city module'''
import unittest
import datetime
import models
from models.city import City
from models.state import State


class TestCity(unittest.TestCase):
    '''Unit tests for city model'''

    @classmethod
    def setUpClass(cls):
        '''Update file path for test'''
        models.storage.update_file_path('test_file.json')

    @classmethod
    def tearDownClass(cls):
        '''Update file path for app'''
        models.storage.update_file_path('file.json')

    def tearDown(self):
        models.storage.reset()

    def test_state_id(self):
        '''Check if id creation wroks well'''
        city_1 = City()
        city_2 = City()
        self.assertIsInstance(city_1, City)
        self.assertTrue(hasattr(city_1, 'id'))
        self.assertIsInstance(city_1.id, str)
        self.assertNotEqual(city_1.id, city_2.id)

    def test_date(self):
        '''Tests for created_at and updated_at attributes'''
        city = City()
        self.assertTrue(hasattr(city, 'created_at'))
        self.assertTrue(hasattr(city, 'updated_at'))
        self.assertIsInstance(city.created_at, datetime.datetime)
        self.assertIsInstance(city.updated_at, datetime.datetime)

    def test_save(self):
        '''Tests for public 'save' method'''
        city = City()
        old_updated_at = city.updated_at
        city.save()
        self.assertTrue(old_updated_at < city.updated_at)

    def test_to_dict(self):
        '''Tests for 'to_dict' method'''
        state = City()
        state_json = state.to_dict()
        self.assertEqual(state_json['__class__'], 'City')
        self.assertEqual(state_json['id'], state.id)
        self.assertEqual(state_json['created_at'],
                         state.created_at.isoformat())
        self.assertEqual(state_json['updated_at'],
                         state.updated_at.isoformat())

    def test_re_create_instance(self):
        '''Tests for re-creating an instance'''
        city = City()
        state = State()
        city.state_id = state.id
        city_json = city.to_dict()
        new_city = City(**city_json)

        self.assertEqual(new_city.state_id, state.id)
        self.assertEqual(new_city.id, city.id)
        self.assertEqual(new_city.created_at, city.created_at)
        self.assertEqual(new_city.updated_at, city.updated_at)

        new_city.save()
        self.assertNotEqual(new_city.updated_at, city.updated_at)

        self.assertFalse(new_city is city)


if __name__ == '__main__':
    unittest.main()
