#!/usr/bin/python3
'''Unit tests for review module'''
import unittest
import datetime
import uuid
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
import models
from models.review import Review
from models.place import Place


class TestReviewBaseModel(unittest.TestCase):
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

    def test_review_id(self):
        '''Check if id creation wroks well'''
        review_1 = Review()
        review_2 = Review()
        self.assertIsInstance(review_1, Review)
        self.assertTrue(hasattr(review_1, 'id'))
        self.assertIsInstance(review_1.id, str)
        self.assertNotEqual(review_1.id, review_2.id)

    def test_date(self):
        '''Tests for created_at and updated_at attributes'''
        review = Review()
        self.assertTrue(hasattr(review, 'created_at'))
        self.assertTrue(hasattr(review, 'updated_at'))
        self.assertIsInstance(review.created_at, datetime.datetime)
        self.assertIsInstance(review.updated_at, datetime.datetime)

    def test_save(self):
        '''Tests for public 'save' method'''
        review = Review()
        old_updated_at = review.updated_at
        key = 'Review.{}'.format(review.id)
        self.assertNotIn(key, models.storage.all().values())
        review.save()
        self.assertIn(key, models.storage.all().keys())
        self.assertTrue(old_updated_at < review.updated_at)

    def test_re_create_instance(self):
        '''Tests for re-creating an instance'''
        review = Review()
        review.number = 98
        review_json = review.to_dict()
        new_review = Review(**review_json)

        self.assertEqual(new_review.id, review.id)
        self.assertEqual(new_review.created_at, review.created_at)
        self.assertEqual(new_review.updated_at, review.updated_at)
        self.assertEqual(new_review.number, review.number)

        new_review.number = 100
        new_review.save()
        self.assertNotEqual(new_review.number, review.number)
        self.assertLess(review.updated_at, new_review.updated_at)

        self.assertFalse(new_review is review)

    def test_to_dict(self):
        '''Tests for 'to_dict' method'''
        review = Review()
        review_json = review.to_dict()
        self.assertEqual(review_json['__class__'], 'Review')
        self.assertEqual(review_json['id'], review.id)
        self.assertEqual(review_json['created_at'],
                         review.created_at.isoformat())
        self.assertEqual(review_json['updated_at'],
                         review.updated_at.isoformat())


class TestReview(unittest.TestCase):
    '''Unit tests for review model'''

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

    def test_review_id(self):
        '''Check if id creation wroks well'''
        review_1 = Review()
        review_2 = Review()
        self.assertIsInstance(review_1, Review)
        self.assertTrue(hasattr(review_1, 'id'))
        self.assertIsInstance(review_1.id, str)
        self.assertNotEqual(review_1.id, review_2.id)

    def test_review_place_id(self):
        '''Check if id creation wroks well'''
        review = Review()
        place = Place()

        review.place_id = place.id

        self.assertIsInstance(review, Review)
        self.assertEqual(review.place_id, place.id)
        self.assertTrue(hasattr(review, 'place_id'))
        self.assertIsInstance(review.place_id, str)

    def test_date(self):
        '''Tests for created_at and updated_at attributes'''
        review = Review()
        self.assertTrue(hasattr(review, 'created_at'))
        self.assertTrue(hasattr(review, 'updated_at'))
        self.assertIsInstance(review.created_at, datetime.datetime)
        self.assertIsInstance(review.updated_at, datetime.datetime)

    def test_save(self):
        '''Tests for public 'save' method'''
        review = Review()
        old_updated_at = review.updated_at
        review.save()
        self.assertTrue(old_updated_at < review.updated_at)

    def test_to_dict(self):
        '''Tests for 'to_dict' method'''
        review = Review()
        review_json = review.to_dict()
        self.assertEqual(review_json['__class__'], 'Review')
        self.assertEqual(review_json['id'], review.id)
        self.assertEqual(review_json['created_at'],
                         review.created_at.isoformat())
        self.assertEqual(review_json['updated_at'],
                         review.updated_at.isoformat())

    def test_re_create_instance(self):
        '''Tests for re-creating an instance'''
        review = Review()
        review_json = review.to_dict()
        new_review = Review(**review_json)

        self.assertEqual(new_review.id, review.id)
        self.assertEqual(new_review.created_at, review.created_at)
        self.assertEqual(new_review.updated_at, review.updated_at)

        new_review.save()
        self.assertNotEqual(new_review.updated_at, review.updated_at)

        self.assertFalse(new_review is review)


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

    def test_show_no_instance_found(self):
        '''Test 'do_show' method with no instance id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show Review 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())

    def test_create_object(self):
        '''Test 'do_create' method'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Review')

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

    def test_count_object(self):
        '''Test 'do_count' method'''
        models.storage.reset()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Review')
            HBNBCommand().onecmd('count Review')

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

    def test_destroy_no_instance(self):
        '''Test 'destroy' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy Review 1')

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

    def test_update_no_instance(self):
        '''Test 'update' method with no instance'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update Review 1')

            msg = '** no instance found **'
            self.assertEqual(msg, f.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
