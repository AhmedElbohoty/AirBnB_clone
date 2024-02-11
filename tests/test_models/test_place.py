#!/usr/bin/python3
'''Unit tests for place module'''
import unittest
import datetime
import models
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.user import User


class TestPlace(unittest.TestCase):
    '''Unit tests for place model'''

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

    def test_place_id(self):
        '''Check if id creation wroks well'''
        place_1 = Place()
        place_2 = Place()
        self.assertIsInstance(place_1, Place)
        self.assertTrue(hasattr(place_1, 'id'))
        self.assertIsInstance(place_1.id, str)
        self.assertNotEqual(place_1.id, place_2.id)

    def test_date(self):
        '''Tests for created_at and updated_at attributes'''
        place = Place()
        self.assertTrue(hasattr(place, 'created_at'))
        self.assertTrue(hasattr(place, 'updated_at'))
        self.assertIsInstance(place.created_at, datetime.datetime)
        self.assertIsInstance(place.updated_at, datetime.datetime)

    def test_save(self):
        '''Tests for public 'save' method'''
        place = Place()
        old_updated_at = place.updated_at
        place.save()
        self.assertTrue(old_updated_at < place.updated_at)

    def test_to_dict(self):
        '''Tests for 'to_dict' method'''
        place = Place()
        place_json = place.to_dict()
        self.assertEqual(place_json['__class__'], 'Place')
        self.assertEqual(place_json['id'], place.id)
        self.assertEqual(place_json['created_at'],
                         place.created_at.isoformat())
        self.assertEqual(place_json['updated_at'],
                         place.updated_at.isoformat())

    def test_re_create_instance(self):
        '''Tests for re-creating an instance'''
        place = Place()
        place_json = place.to_dict()
        new_place = Place(**place_json)

        self.assertEqual(new_place.id, place.id)
        self.assertEqual(new_place.created_at, place.created_at)
        self.assertEqual(new_place.updated_at, place.updated_at)

        city = City()
        amenity = Amenity()
        user = User()
        new_place.city_id = city.id
        new_place.amenity_ids = [amenity.id]
        new_place.user_id = user.id
        new_place.save()
        self.assertEqual(new_place.city_id, city.id)
        self.assertEqual(new_place.user_id, user.id)
        self.assertEqual(new_place.amenity_ids, [amenity.id])
        self.assertNotEqual(new_place.updated_at, place.updated_at)

        self.assertFalse(new_place is place)


if __name__ == '__main__':
    unittest.main()
