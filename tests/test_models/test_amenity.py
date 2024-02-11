#!/usr/bin/python3
'''Unit tests for amenity module'''
import unittest
import datetime
import models
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    '''Unit tests for amenity model'''

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

    def test_amenity_id(self):
        '''Check if id creation wroks well'''
        amenity_1 = Amenity()
        amenity_2 = Amenity()
        self.assertIsInstance(amenity_1, Amenity)
        self.assertTrue(hasattr(amenity_1, 'id'))
        self.assertIsInstance(amenity_1.id, str)
        self.assertNotEqual(amenity_1.id, amenity_2.id)

    def test_date(self):
        '''Tests for created_at and updated_at attributes'''
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, 'created_at'))
        self.assertTrue(hasattr(amenity, 'updated_at'))
        self.assertIsInstance(amenity.created_at, datetime.datetime)
        self.assertIsInstance(amenity.updated_at, datetime.datetime)

    def test_save(self):
        '''Tests for public 'save' method'''
        amenity = Amenity()
        old_updated_at = amenity.updated_at
        amenity.save()
        self.assertTrue(old_updated_at < amenity.updated_at)

    def test_to_dict(self):
        '''Tests for 'to_dict' method'''
        amenity = Amenity()
        amenity_json = amenity.to_dict()
        self.assertEqual(amenity_json['__class__'], 'Amenity')
        self.assertEqual(amenity_json['id'], amenity.id)
        self.assertEqual(amenity_json['created_at'],
                         amenity.created_at.isoformat())
        self.assertEqual(amenity_json['updated_at'],
                         amenity.updated_at.isoformat())

    def test_re_create_instance(self):
        '''Tests for re-creating an instance'''
        amenity = Amenity()
        amenity_json = amenity.to_dict()
        new_amenity = Amenity(**amenity_json)

        self.assertEqual(new_amenity.id, amenity.id)
        self.assertEqual(new_amenity.created_at, amenity.created_at)
        self.assertEqual(new_amenity.updated_at, amenity.updated_at)

        new_amenity.save()
        self.assertNotEqual(new_amenity.updated_at, amenity.updated_at)

        self.assertFalse(new_amenity is amenity)


if __name__ == '__main__':
    unittest.main()
