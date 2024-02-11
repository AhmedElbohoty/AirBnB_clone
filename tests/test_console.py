#!/usr/bin/python3
'''Unit tests for base model module'''
import unittest
import uuid
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
import models


class TestHBNBCommand(unittest.TestCase):
    '''Unit tests for hbnb command'''

    @classmethod
    def setUpClass(cls):
        '''Update file path for test'''
        models.storage.update_file_path('test_file.json')

    @classmethod
    def tearDownClass(cls):
        '''Update file path for app'''
        models.storage.update_file_path('file.json')

    def test_help(self):
        '''Tests for 'help' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('help quit')

            msg = 'Exit the program with \'quit\' command'
            self.assertEqual(msg, f.getvalue().strip())

    # def test_quit(self):
    #     '''Tests for 'quit' method'''
    #     with patch('sys.stdout', new=StringIO()):
    #         self.assertTrue(HBNBCommand().onecmd('quit'))

    # def test_EOF(self):
    #     '''Tests for 'EOF' method'''
    #     with patch('sys.stdout', new=StringIO()):
    #         self.assertTrue(HBNBCommand().onecmd('EOF'))

    def test_empty(self):
        '''Tests for empty line'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('')
            self.assertEqual('', f.getvalue().strip())


class TestHBNBCommandBaseModel(unittest.TestCase):
    '''Unit tests for hbnb command - BaseModel'''

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
            HBNBCommand().onecmd('show BaseModel')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_missing_id_class_method(self):
        '''Test 'BaseModel.show' method with missing id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.show()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found(self):
        '''Test 'do_show' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show BaseModel 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found_class_method(self):
        '''Test 'BaseModel.show(1)' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.show(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_create_object(self):
        '''Test 'do_create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create BaseModel')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_create_object_class_method(self):
        '''Test 'create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.create()')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_show_object(self):
        '''Test 'do_show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create BaseModel')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('show BaseModel {}'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[BaseModel] ({})'.format(obj_id)))

    def test_show_object_class_method(self):
        '''Test 'show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('BaseModel.show({})'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[BaseModel] ({})'.format(obj_id)))

    def test_count_object(self):
        '''Test 'do_count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create BaseModel')
            HBNBCommand().onecmd('count BaseModel')

            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

    def test_count_object_class_method(self):
        '''Test 'count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.create()')
            HBNBCommand().onecmd('BaseModel.count()')

            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

    def test_destroy_no_class(self):
        '''Test 'destroy' method with no class'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('destroy'))

            msg = '** class name missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_invalid_class(self):
        '''Test 'destroy' method with invalid class'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('destroy InvalidModel'))

            msg = '** class doesn\'t exist **'
            self.assertEqual(msg, f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('InvalidModel.destroy()'))

            msg = '** class doesn\'t exist **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing(self):
        '''Test 'destroy' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('destroy BaseModel'))

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'BaseModel.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('BaseModel.destroy()'))

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('destroy BaseModel 1'))

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'BaseModel.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('BaseModel.destroy(1)'))

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_objects(self):
        '''Test 'destroy' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create BaseModel')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count BaseModel')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('destroy BaseModel {}'.format(obj_id))
            HBNBCommand().onecmd('count BaseModel')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')

    def test_destroy_objects_class_method(self):
        '''Test 'BaseModel.destroy()' '''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count BaseModel')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('BaseModel.destroy({})'.format(obj_id))
            HBNBCommand().onecmd('count BaseModel')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')


if __name__ == '__main__':
    unittest.main()
