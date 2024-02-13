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

    def tearDown(self):
        models.storage.reset()

    def test_help(self):
        '''Tests for 'help' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('help quit')

            msg = 'Exit the program with \'quit\' command'
            self.assertEqual(msg, f.getvalue().strip())

    # def test_quit(self):
    #     '''Tests for 'quit' method'''
    #     with patch('sys.stdout', new=StringIO()):
    #         self.assertTrue(HBNBCommand().onecmd('quit')

    # def test_EOF(self):
    #     '''Tests for 'EOF' method'''
    #     with patch('sys.stdout', new=StringIO()):
    #         self.assertTrue(HBNBCommand().onecmd('EOF')

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

    def test_class_all(self):
        '''Test 'BaseModel.all()' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.all()')
            output = f.getvalue().strip()
            self.assertEqual(output, '[]')

            HBNBCommand().onecmd('create BaseModel')

            HBNBCommand().onecmd('BaseModel.all()')
            obj_id = f.getvalue().split('\n')[1].strip()
            output = f.getvalue().split('\n')[2].strip()
            self.assertTrue('["[BaseModel] ({})'.format(obj_id) in output)

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
            HBNBCommand().onecmd('destroy BaseModel')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'BaseModel.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.destroy()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy BaseModel 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'BaseModel.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.destroy(1)')

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
            HBNBCommand().onecmd('update BaseModel')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_id_missing_class_method(self):
        '''Test 'BaseModel.update()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.update()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance(self):
        '''Test 'update' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance_class_method(self):
        '''Test 'BaseModel.update()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.update(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())


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

    def test_class_all(self):
        '''Test 'User.all()' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.all()')
            output = f.getvalue().strip()
            self.assertEqual(output, '[]')

            HBNBCommand().onecmd('create User')

            HBNBCommand().onecmd('User.all()')
            obj_id = f.getvalue().split('\n')[1].strip()
            output = f.getvalue().split('\n')[2].strip()
            self.assertTrue('["[User] ({})'.format(obj_id) in output)

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
            HBNBCommand().onecmd('destroy User')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'User.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.destroy()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy User 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'User.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.destroy(1)')

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
            HBNBCommand().onecmd('update User')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_id_missing_class_method(self):
        '''Test 'User.update()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.update()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance(self):
        '''Test 'update' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update User 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance_class_method(self):
        '''Test 'User.update()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('User.update(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())


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

    def test_class_all(self):
        '''Test 'Amenity.all()' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.all()')
            output = f.getvalue().strip()
            self.assertEqual(output, '[]')

            HBNBCommand().onecmd('create Amenity')

            HBNBCommand().onecmd('Amenity.all()')
            obj_id = f.getvalue().split('\n')[1].strip()
            output = f.getvalue().split('\n')[2].strip()
            self.assertTrue('["[Amenity] ({})'.format(obj_id) in output)

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
            HBNBCommand().onecmd('destroy Amenity')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'Amenity.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.destroy()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy Amenity 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'Amenity.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.destroy(1)')

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
            HBNBCommand().onecmd('update Amenity')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_id_missing_class_method(self):
        '''Test 'Amenity.update()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.update()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance(self):
        '''Test 'update' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update Amenity 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance_class_method(self):
        '''Test 'Amenity.update()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.update(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())


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
            HBNBCommand().onecmd('destroy City')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'City.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('City.destroy()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy City 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'City.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('City.destroy(1)')

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
            HBNBCommand().onecmd('update City')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_id_missing_class_method(self):
        '''Test 'City.update()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('City.update()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance(self):
        '''Test 'update' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update City 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance_class_method(self):
        '''Test 'City.update()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('City.update(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())


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
            HBNBCommand().onecmd('destroy Place')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'Place.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Place.destroy()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy Place 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'Place.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Place.destroy(1)')

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
            HBNBCommand().onecmd('update Place')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_id_missing_class_method(self):
        '''Test 'Place.update()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Place.update()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance(self):
        '''Test 'update' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update Place 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance_class_method(self):
        '''Test 'Place.update()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Place.update(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())


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

    def test_show_missing_id_class_method(self):
        '''Test 'State.show' method with missing id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('State.show()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found(self):
        '''Test 'do_show' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show State 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found_class_method(self):
        '''Test 'State.show(1)' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('State.show(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_create_object(self):
        '''Test 'do_create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_create_object_class_method(self):
        '''Test 'create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('State.create()')

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

    def test_show_object_class_method(self):
        '''Test 'show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('State.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('State.show({})'.format(obj_id))

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

    def test_count_object_class_method(self):
        '''Test 'count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('State.create()')
            HBNBCommand().onecmd('State.count()')

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

    def test_destroy_id_missing_class_method(self):
        '''Test 'State.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('State.destroy()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy State 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'State.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('State.destroy(1)')

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

    def test_destroy_objects_class_method(self):
        '''Test 'State.destroy()' '''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('State.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count State')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('State.destroy({})'.format(obj_id))
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

    def test_update_id_missing_class_method(self):
        '''Test 'State.update()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('State.update()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance(self):
        '''Test 'update' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update State 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance_class_method(self):
        '''Test 'State.update()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('State.update(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())


class TestHBNBCommandReview(unittest.TestCase):
    '''Unit tests for hbnb command - Review'''

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
            HBNBCommand().onecmd('show Review')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_missing_id_class_method(self):
        '''Test 'Review.show' method with missing id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Review.show()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found(self):
        '''Test 'do_show' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show Review 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_show_no_instance_found_class_method(self):
        '''Test 'Review.show(1)' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Review.show(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_create_object(self):
        '''Test 'do_create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Review')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_create_object_class_method(self):
        '''Test 'create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Review.create()')

            obj_id = f.getvalue().strip()
            self.assertTrue(uuid.UUID(str(obj_id)))

    def test_show_object(self):
        '''Test 'do_show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Review')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('show Review {}'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[Review] ({})'.format(obj_id)))

    def test_show_object_class_method(self):
        '''Test 'show' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Review.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('Review.show({})'.format(obj_id))

            obj = f.getvalue().split('\n')[1].strip()
            self.assertTrue(obj.startswith('[Review] ({})'.format(obj_id)))

    def test_count_object(self):
        '''Test 'do_count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Review')
            HBNBCommand().onecmd('count Review')

            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

    def test_count_object_class_method(self):
        '''Test 'count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Review.create()')
            HBNBCommand().onecmd('Review.count()')

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
            HBNBCommand().onecmd('destroy Review')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_id_missing_class_method(self):
        '''Test 'Review.destroy()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Review.destroy()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy Review 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_no_instance_class_method(self):
        '''Test 'Review.destroy()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Review.destroy(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_destroy_objects(self):
        '''Test 'destroy' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Review')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count Review')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('destroy Review {}'.format(obj_id))
            HBNBCommand().onecmd('count Review')
            count = f.getvalue().split('\n')[2].strip()
            self.assertEqual(count, '0')

    def test_destroy_objects_class_method(self):
        '''Test 'Review.destroy()' '''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Review.create()')
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd('count Review')
            count = f.getvalue().split('\n')[1].strip()
            self.assertEqual(count, '1')

            HBNBCommand().onecmd('Review.destroy({})'.format(obj_id))
            HBNBCommand().onecmd('count Review')
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
            HBNBCommand().onecmd('update Review')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_id_missing_class_method(self):
        '''Test 'Review.update()' method with no id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Review.update()')

            msg = '** instance id missing **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance(self):
        '''Test 'update' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update Review 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_update_no_instance_class_method(self):
        '''Test 'Review.update()' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Review.update(1)')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
