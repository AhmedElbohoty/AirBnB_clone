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
        '''Tests for public method save'''
        bm = BaseModel()
        old_updated_at = bm.updated_at
        bm.save()
        self.assertTrue(old_updated_at < bm.updated_at)


if __name__ == '__main__':
    unittest.main()
