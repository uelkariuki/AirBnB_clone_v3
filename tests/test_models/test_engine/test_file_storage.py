#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    def test_get_existing_object(self):
        '''Create and add an object to the database'''
        user = User(name="John")
        self.db_storage.new(user)
        self.db_storage.save()

        retrieved_user = self.db_storage.get(User, user.id)

        self.assertEqual(retrieved_user, user)

    def test_get_nonexistent_object(self):
        '''Attempt to retrieve a non-existent object'''
        retrieved_user = self.db_storage.get(User, "nonexistent_id")

        self.assertIsNone(retrieved_user)

    def test_get_invalid_class_argument(self):
        '''Attempt to retrieve an object with an invalid class argument'''
        retrieved_object = self.db_storage.get(SomeOtherClass, "some_id")

        self.assertIsNone(retrieved_object)

    def test_count_all_objects(self):
        '''Create and add objects of different classes to the database'''
        user = User(name="John")
        some_other_object = SomeOtherClass(name="Example")
        self.db_storage.new(user)
        self.db_storage.new(some_other_object)
        self.db_storage.save()

        total_count = self.db_storage.count()

        self.assertEqual(total_count, 2)

    def test_count_objects_of_specific_class(self):
        '''Create and add objects of the same class to the database'''
        user1 = User(name="John")
        user2 = User(name="Alice")
        self.db_storage.new(user1)
        self.db_storage.new(user2)
        self.db_storage.save()

        user_count = self.db_storage.count(User)

        self.assertEqual(user_count, 2)

    def test_count_nonexistent_class(self):
        '''Attempt to count objects of a class that does not exist'''
        count = self.db_storage.count(NonExistentClass)

        # Verify that the method returns 0 or handles the error gracefully
        self.assertEqual(count, 0)

    def test_count_objects_in_empty_database(self):
        '''Create an instance of DBStorage with an empty database'''
        db_storage_empty = DBStorage()

        total_count = db_storage_empty.count()

        self.assertEqual(total_count, 0)
