#!/usr/bin/python3
'''Unit tests for user module'''
import unittest
import datetime
import models
from models.user import User


class TestUserBaseModel(unittest.TestCase):
    '''Unit tests for methods and attributes inherited from base model'''

    @classmethod
    def setUpClass(cls):
        '''Update file path for test'''
        models.storage.update_file_path('test_file.json')

    @classmethod
    def tearDownClass(cls):
        '''Update file path for app'''
        models.storage.update_file_path('file.json')

    def test_user_id(self):
        '''Check if id creation wroks well'''
        user_1 = User()
        user_2 = User()
        self.assertIsInstance(user_1, User)
        self.assertTrue(hasattr(user_1, 'id'))
        self.assertIsInstance(user_1.id, str)
        self.assertNotEqual(user_1.id, user_2.id)

    def test_date(self):
        '''Tests for created_at and updated_at attributes'''
        user = User()
        self.assertTrue(hasattr(user, 'created_at'))
        self.assertTrue(hasattr(user, 'updated_at'))
        self.assertIsInstance(user.created_at, datetime.datetime)
        self.assertIsInstance(user.updated_at, datetime.datetime)

    def test_save(self):
        '''Tests for public 'save' method'''
        user = User()
        old_updated_at = user.updated_at
        key = 'User.{}'.format(user.id)
        self.assertNotIn(key, models.storage.all().values())
        user.save()
        self.assertIn(key, models.storage.all().keys())
        self.assertTrue(old_updated_at < user.updated_at)

    def test_re_create_instance(self):
        '''Tests for re-creating an instance'''
        user = User()
        user.number = 98
        user_json = user.to_dict()
        new_user = User(**user_json)

        self.assertEqual(new_user.id, user.id)
        self.assertEqual(new_user.created_at, user.created_at)
        self.assertEqual(new_user.updated_at, user.updated_at)
        self.assertEqual(new_user.number, user.number)

        new_user.number = 100
        new_user.save()
        self.assertNotEqual(new_user.number, user.number)
        self.assertLess(user.updated_at, new_user.updated_at)

        self.assertFalse(new_user is user)

    def test_to_dict(self):
        '''Tests for 'to_dict' method'''
        user = User()
        user_json = user.to_dict()
        self.assertEqual(user_json['__class__'], 'User')
        self.assertEqual(user_json['id'], user.id)
        self.assertEqual(user_json['created_at'], user.created_at.isoformat())
        self.assertEqual(user_json['updated_at'], user.updated_at.isoformat())


class TestUser(unittest.TestCase):
    '''Unit tests for user model'''

    @classmethod
    def setUpClass(cls):
        '''Update file path for test'''
        models.storage.update_file_path('test_file.json')

    @classmethod
    def tearDownClass(cls):
        '''Update file path for app'''
        models.storage.update_file_path('file.json')

    def test_create_user_no_args(self):
        '''Create user with no args'''
        self.assertEqual(User, type(User()))

    def test_user_names(self):
        '''Tests for first_name and last_name attributes'''
        user = User()
        self.assertTrue(hasattr(user, 'first_name'))
        self.assertTrue(hasattr(user, 'last_name'))
        self.assertTrue(user.first_name == '')
        self.assertTrue(user.last_name == '')
        user.first_name = 'Ahmed'
        user.last_name = 'Elbohoty'
        self.assertEqual(user.first_name, 'Ahmed')
        self.assertEqual(user.last_name, 'Elbohoty')

    def test_user_email(self):
        '''Tests for email attribute'''
        user = User()
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(user.email == '')
        user.email = 'ahmed@email.com'
        self.assertEqual(user.email, 'ahmed@email.com')

    def test_password(self):
        '''Tests for first and last name attribute'''
        user = User()
        self.assertTrue(hasattr(user, 'password'))
        self.assertTrue(user.email == '')
        user.password = '0000'
        self.assertEqual(user.password, '0000')

    def test_to_dict(self):
        '''Tests for 'to_dict' method'''
        user = User()
        user.first_name = 'Ahmed'
        user.last_name = 'Elbohoty'
        user.email = 'ahmed@email.com'
        user.password = '0000'
        user_json = user.to_dict()
        self.assertEqual(user_json['first_name'], user.first_name)
        self.assertEqual(user_json['last_name'], user.last_name)
        self.assertEqual(user_json['email'], user.email)
        self.assertEqual(user_json['password'], user.password)


if __name__ == '__main__':
    unittest.main()
