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


class TestHBNBCommandUser(unittest.TestCase):
    '''Unit tests for hbnb command - User'''

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
            HBNBCommand().onecmd('show User')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_missing_id_class_method(self):
        '''Test 'User.show' method with missing id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.show()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found(self):
        '''Test 'do_show' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show User 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found_class_method(self):
        '''Test 'User.show(1)' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.show(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_create_object(self):
        '''Test 'do_create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_create_object_class_method(self):
        '''Test 'create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.create()')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_show_object(self):
        '''Test 'do_show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('show User {}'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[User] ({})'.format(obj_id)))

    def test_show_object_class_method(self):
        '''Test 'show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('User.show({})'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[User] ({})'.format(obj_id)))

    def test_count_object(self):
        '''Test 'do_count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User')
            HBNBCommand().onecmd('count User')

            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

    def test_count_object_class_method(self):
        '''Test 'count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.create()')
            HBNBCommand().onecmd('User.count()')

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
            self.assertFalse(HBNBCommand().onecmd('destroy User'))

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'User.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('User.destroy()'))

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('destroy User 1'))

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'User.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('User.destroy(1)'))

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_objects(self):
        '''Test 'destroy' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count User')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('destroy User {}'.format(obj_id))
            HBNBCommand().onecmd('count User')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')

    def test_destroy_objects_class_method(self):
        '''Test 'User.destroy()' '''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count User')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('User.destroy({})'.format(obj_id))
            HBNBCommand().onecmd('count User')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')


class TestHBNBCommandAmenity(unittest.TestCase):
    '''Unit tests for hbnb command - Amenity'''

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
            HBNBCommand().onecmd('show Amenity')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_missing_id_class_method(self):
        '''Test 'Amenity.show' method with missing id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.show()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found(self):
        '''Test 'do_show' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show Amenity 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found_class_method(self):
        '''Test 'Amenity.show(1)' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.show(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_create_object(self):
        '''Test 'do_create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Amenity')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_create_object_class_method(self):
        '''Test 'create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.create()')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_show_object(self):
        '''Test 'do_show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Amenity')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('show Amenity {}'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[Amenity] ({})'.format(obj_id)))

    def test_show_object_class_method(self):
        '''Test 'show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('Amenity.show({})'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[Amenity] ({})'.format(obj_id)))

    def test_count_object(self):
        '''Test 'do_count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Amenity')
            HBNBCommand().onecmd('count Amenity')

            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

    def test_count_object_class_method(self):
        '''Test 'count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.create()')
            HBNBCommand().onecmd('Amenity.count()')

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
            self.assertFalse(HBNBCommand().onecmd('destroy Amenity'))

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'Amenity.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('Amenity.destroy()'))

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('destroy Amenity 1'))

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'Amenity.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('Amenity.destroy(1)'))

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_objects(self):
        '''Test 'destroy' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Amenity')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count Amenity')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('destroy Amenity {}'.format(obj_id))
            HBNBCommand().onecmd('count Amenity')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')

    def test_destroy_objects_class_method(self):
        '''Test 'Amenity.destroy()' '''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count Amenity')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('Amenity.destroy({})'.format(obj_id))
            HBNBCommand().onecmd('count Amenity')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')


class TestHBNBCommandCity(unittest.TestCase):
    '''Unit tests for hbnb command - City'''

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
            HBNBCommand().onecmd('show City')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_missing_id_class_method(self):
        '''Test 'City.show' method with missing id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('City.show()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found(self):
        '''Test 'do_show' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show City 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found_class_method(self):
        '''Test 'City.show(1)' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('City.show(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_create_object(self):
        '''Test 'do_create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create City')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_create_object_class_method(self):
        '''Test 'create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('City.create()')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_show_object(self):
        '''Test 'do_show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create City')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('show City {}'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[City] ({})'.format(obj_id)))

    def test_show_object_class_method(self):
        '''Test 'show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('City.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('City.show({})'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[City] ({})'.format(obj_id)))

    def test_count_object(self):
        '''Test 'do_count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create City')
            HBNBCommand().onecmd('count City')

            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

    def test_count_object_class_method(self):
        '''Test 'count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('City.create()')
            HBNBCommand().onecmd('City.count()')

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
            self.assertFalse(HBNBCommand().onecmd('destroy City'))

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'City.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('City.destroy()'))

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('destroy City 1'))

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'City.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('City.destroy(1)'))

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_objects(self):
        '''Test 'destroy' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create City')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count City')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('destroy City {}'.format(obj_id))
            HBNBCommand().onecmd('count City')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')

    def test_destroy_objects_class_method(self):
        '''Test 'City.destroy()' '''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('City.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count City')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('City.destroy({})'.format(obj_id))
            HBNBCommand().onecmd('count City')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')


class TestHBNBCommandPlace(unittest.TestCase):
    '''Unit tests for hbnb command - Place'''

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
            HBNBCommand().onecmd('show Place')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_missing_id_class_method(self):
        '''Test 'Place.show' method with missing id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Place.show()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found(self):
        '''Test 'do_show' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show Place 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found_class_method(self):
        '''Test 'Place.show(1)' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Place.show(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_create_object(self):
        '''Test 'do_create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Place')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_create_object_class_method(self):
        '''Test 'create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Place.create()')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_show_object(self):
        '''Test 'do_show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Place')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('show Place {}'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[Place] ({})'.format(obj_id)))

    def test_show_object_class_method(self):
        '''Test 'show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Place.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('Place.show({})'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[Place] ({})'.format(obj_id)))

    def test_count_object(self):
        '''Test 'do_count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Place')
            HBNBCommand().onecmd('count Place')

            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

    def test_count_object_class_method(self):
        '''Test 'count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Place.create()')
            HBNBCommand().onecmd('Place.count()')

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
            self.assertFalse(HBNBCommand().onecmd('destroy Place'))

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'Place.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('Place.destroy()'))

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('destroy Place 1'))

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'Place.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd('Place.destroy(1)'))

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_objects(self):
        '''Test 'destroy' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Place')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count Place')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('destroy Place {}'.format(obj_id))
            HBNBCommand().onecmd('count Place')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')

    def test_destroy_objects_class_method(self):
        '''Test 'Place.destroy()' '''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Place.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count Place')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('Place.destroy({})'.format(obj_id))
            HBNBCommand().onecmd('count Place')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')


if __name__ == '__main__':
    unittest.main()
