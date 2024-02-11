#!/usr/bin/python3
'''Unit tests for state module'''
import unittest
import datetime
import models
from models.state import State


class TestState(unittest.TestCase):
    '''Unit tests for state model'''

    @classmethod
    def setUpClass(cls):
        '''Update file path for test'''
        models.storage.update_file_path('test_file.json')

    @classmethod
    def tearDownClass(cls):
        '''Update file path for app'''
        models.storage.update_file_path('file.json')

    def test_state_id(self):
        '''Check if id creation wroks well'''
        state_1 = State()
        state_2 = State()
        self.assertIsInstance(state_1, State)
        self.assertTrue(hasattr(state_1, 'id'))
        self.assertIsInstance(state_1.id, str)
        self.assertNotEqual(state_1.id, state_2.id)

    def test_date(self):
        '''Tests for created_at and updated_at attributes'''
        state = State()
        self.assertTrue(hasattr(state, 'created_at'))
        self.assertTrue(hasattr(state, 'updated_at'))
        self.assertIsInstance(state.created_at, datetime.datetime)
        self.assertIsInstance(state.updated_at, datetime.datetime)

    def test_save(self):
        '''Tests for public 'save' method'''
        state = State()
        old_updated_at = state.updated_at
        state.save()
        self.assertTrue(old_updated_at < state.updated_at)

    def test_to_dict(self):
        '''Tests for 'to_dict' method'''
        state = State()
        state_json = state.to_dict()
        self.assertEqual(state_json['__class__'], 'State')
        self.assertEqual(state_json['id'], state.id)
        self.assertEqual(state_json['created_at'],
                         state.created_at.isoformat())
        self.assertEqual(state_json['updated_at'],
                         state.updated_at.isoformat())

    def test_re_create_instance(self):
        '''Tests for re-creating an instance'''
        state = State()
        state_json = state.to_dict()
        new_state = State(**state_json)

        self.assertEqual(new_state.id, state.id)
        self.assertEqual(new_state.created_at, state.created_at)
        self.assertEqual(new_state.updated_at, state.updated_at)

        new_state.save()
        self.assertNotEqual(new_state.updated_at, state.updated_at)

        self.assertFalse(new_state is state)


if __name__ == '__main__':
    unittest.main()
