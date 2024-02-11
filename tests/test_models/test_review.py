#!/usr/bin/python3
'''Unit tests for review module'''
import unittest
import datetime
import models
from models.review import Review


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


if __name__ == '__main__':
    unittest.main()
