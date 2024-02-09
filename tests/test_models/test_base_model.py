#!/usr/bin/python3
'''Unit tests for base model'''
import unittest
from models.base_model import BaseModel
import datetime


class TestBaseModel(unittest.TestCase):
    '''Unit tests for base model'''

    def test_base_model_id(self):
        '''Check if id creation wroks well'''
        bm_1 = BaseModel()
        bm_2 = BaseModel()
        self.assertIsInstance(bm_1, BaseModel)
        self.assertTrue(hasattr(bm_1, 'id'))
        self.assertIsInstance(bm_1.id, str)
        self.assertNotEqual(bm_1.id, bm_2.id)

    def test_date(self):
        '''Tests for created_at and updated_at attributes'''
        bm = BaseModel()
        self.assertTrue(hasattr(bm, 'created_at'))
        self.assertTrue(hasattr(bm, 'updated_at'))
        self.assertIsInstance(bm.created_at, datetime.datetime)
        self.assertIsInstance(bm.updated_at, datetime.datetime)

    def test_save(self):
        '''Tests for public 'save' method'''
        bm = BaseModel()
        old_updated_at = bm.updated_at
        bm.save()
        self.assertTrue(old_updated_at < bm.updated_at)

    def test_to_dict(self):
        '''Tests for 'to_dict' method'''
        bm = BaseModel()
        bm.number = 98
        bm_json = bm.to_dict()
        self.assertEqual(bm_json['__class__'], 'BaseModel')
        self.assertEqual(bm_json['id'], bm.id)
        self.assertEqual(bm_json['created_at'], bm.created_at.isoformat())
        self.assertEqual(bm_json['updated_at'], bm.updated_at.isoformat())
        self.assertEqual(bm_json['number'], bm.number)

    def test_re_create_instance(self):
        '''Tests for re-creating an instance'''
        bm = BaseModel()
        bm.number = 98
        bm_json = bm.to_dict()
        new_bm = BaseModel(**bm_json)

        self.assertEqual(new_bm.id, bm.id)
        self.assertEqual(new_bm.created_at, bm.created_at)
        self.assertEqual(new_bm.updated_at, bm.updated_at)
        self.assertEqual(new_bm.number, bm.number)

        new_bm.number = 100
        new_bm.save()
        self.assertNotEqual(new_bm.number, bm.number)
        self.assertNotEqual(new_bm.updated_at, bm.updated_at)

        self.assertFalse(new_bm is bm)


if __name__ == '__main__':
    unittest.main()
