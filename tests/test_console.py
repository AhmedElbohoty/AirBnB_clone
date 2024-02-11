#!/usr/bin/python3
'''Unit tests for base model module'''
import unittest
import os
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
        with patch('sys.stdout', new=StringIO()) as output:
            msg = 'Exit the program with \'quit\' command'
            self.assertFalse(HBNBCommand().onecmd('help quit'))
            self.assertEqual(msg, output.getvalue().strip())

    def test_quit(self):
        '''Tests for 'quit' method'''
        with patch('sys.stdout', new=StringIO()):
            self.assertTrue(HBNBCommand().onecmd('quit'))

    def test_EOF(self):
        '''Tests for 'EOF' method'''
        with patch('sys.stdout', new=StringIO()):
            self.assertTrue(HBNBCommand().onecmd('EOF'))

    def test_empty(self):
        '''Tests for empty line'''
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(''))
            self.assertEqual('', output.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
