#!/usr/bin/python3
'''Unit tests for state module'''
import unittest
import datetime
import uuid
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
import models
from models.state import State


class TestStateBaseModel(unittest.TestCase):
    '''Unit tests for methods and attributes inherited from base model'''

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
        key = 'State.{}'.format(state.id)
        self.assertNotIn(key, models.storage.all().values())
        state.save()
        self.assertIn(key, models.storage.all().keys())
        self.assertTrue(old_updated_at < state.updated_at)

    def test_re_create_instance(self):
        '''Tests for re-creating an instance'''
        state = State()
        state.number = 98
        state_json = state.to_dict()
        new_state = State(**state_json)

        self.assertEqual(new_state.id, state.id)
        self.assertEqual(new_state.created_at, state.created_at)
        self.assertEqual(new_state.updated_at, state.updated_at)
        self.assertEqual(new_state.number, state.number)

        new_state.number = 100
        new_state.save()
        self.assertNotEqual(new_state.number, state.number)
        self.assertLess(state.updated_at, new_state.updated_at)

        self.assertFalse(new_state is state)

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

    def tearDown(self):
        models.storage.reset()

    def test_create_user_no_args(self):
        '''Create user with no args'''
        self.assertEqual(State, type(State()))

    def test_state_name(self):
        '''Tests for name attribute'''
        state = State()
        self.assertTrue(hasattr(state, 'name'))
        self.assertTrue(state.name == '')
        state.name = 'state name'
        self.assertEqual(state.name, 'state name')

    def test_to_dict(self):
        '''Tests for 'to_dict' method'''
        state = State()
        state.name = 'state name'
        state_json = state.to_dict()
        self.assertEqual(state_json['name'], state.name)


class TestHBNBCommandState(unittest.TestCase):
    '''Unit tests for hbnb command - State'''

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

    def test_show_missing_id(self):
        '''Test 'do_show' method with missing id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show State')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found(self):
        '''Test 'do_show' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show State 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_create_object(self):
        '''Test 'do_create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_show_object(self):
        '''Test 'do_show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('show State {}'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[State] ({})'.format(obj_id)))

    def test_count_object(self):
        '''Test 'do_count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State')
            HBNBCommand().onecmd('count State')

            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

    def test_destroy_no_class(self):
        '''Test 'destroy' method with no class'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy')

            msg = '** class name missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_invalid_class(self):
        '''Test 'destroy' method with invalid class'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy InvalidModel')

            msg = '** class doesn\'t exist **'
            self.assertEqual(msg, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('InvalidModel.destroy()')

            msg = '** class doesn\'t exist **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing(self):
        '''Test 'destroy' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy State')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy State 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_objects(self):
        '''Test 'destroy' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count State')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('destroy State {}'.format(obj_id))
            HBNBCommand().onecmd('count State')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')

    def test_update_no_class(self):
        '''Test 'update' method with no class'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update')

            msg = '** class name missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_invalid_class(self):
        '''Test 'update' method with invalid class'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update InvalidModel')

            msg = '** class doesn\'t exist **'
            self.assertEqual(msg, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('InvalidModel.update()')

            msg = '** class doesn\'t exist **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_id_missing(self):
        '''Test 'update' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update State')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance(self):
        '''Test 'update' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update State 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
