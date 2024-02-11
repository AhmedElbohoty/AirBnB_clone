#!/usr/bin/python3
'''Unit tests for base model module'''
import unittest
import datetime
from time import sleep
import models
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    '''Unit tests for base model'''

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

    def test_two_objects_created_at(self):
        '''Test objects created_at date'''
        bm_1 = BaseModel()
        sleep(0.01)
        bm_2 = BaseModel()
        self.assertLess(bm_1.created_at, bm_2.created_at)

    def test_two_objects_updated_at(self):
        '''Test objects updated_at date'''
        bm_1 = BaseModel()
        sleep(0.01)
        bm_2 = BaseModel()
        self.assertLess(bm_1.updated_at, bm_2.updated_at)

    def test_save(self):
        '''Tests for public 'save' method'''
        bm = BaseModel()
        old_updated_at = bm.updated_at
        bm.save()
        self.assertTrue(old_updated_at < bm.updated_at)

    def test_save_no_args(self):
        '''Tests for public 'save' method with no args'''

        with self.assertRaises(TypeError) as e:
            BaseModel.save()
        msg = 'BaseModel.save() missing 1 required positional argument: \'self\''
        self.assertEqual(str(e.exception), msg)

    def test_save_extra_arg(self):
        '''Tests for public 'save' method with extra arg'''
        with self.assertRaises(TypeError) as e:
            BaseModel.save(self, '000')
        msg = 'BaseModel.save() takes 1 positional argument but 2 were given'
        self.assertEqual(str(e.exception), msg)

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

    def test___str__(self):
        '''Test string representation for BaseModel'''
        bm = BaseModel()
        string = str(bm)

        instance_id = bm.id
        classname = bm.__class__.__name__
        instance_dict = bm.__dict__

        self.assertEqual(string, '[{}] ({}) {}'.format(
            classname, instance_id, instance_dict))
        self.assertIn('[BaseModel]', string)
        self.assertIn('id', string)
        self.assertIn('created_at', string)
        self.assertIn('updated_at', string)


if __name__ == '__main__':
    unittest.main()
