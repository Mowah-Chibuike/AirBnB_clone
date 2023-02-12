#!/usr/bin/python3
"""
Module contains the FileStorage class
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """
    FileStorage Class
    """

    __file_path = "./file.json"
    __objects = {}
    __class_dict = {'BaseModel': BaseModel, 'User': User, 'Place': Place, 'State': State, 'City': City, 'Amenity': Amenity, 'Review': Review}

    def all(self):
        """
        Return __objects
        """
        return self.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        serializes __objects to the JSON file
        """
        with open(self.__file_path, mode='w+', encoding='utf-8') as file:
            obj_to_dict = {}
            for key, value in self.__objects.items():
                obj_to_dict[key] = value.to_dict()
            json.dump(obj_to_dict, file)

    def reload(self):
        """
        deserializes the JSON file to __objects (only if the JSON file \
        (__file_path) exists ; otherwise, do nothing. If the file doesn’t\
        exist, no exception should be raised
        """
        try:
            with open(self.__file_path, mode='r', encoding='utf-8') as file:
                file.seek(0, 0)
                dict_loaded = json.load(file)
                for key, value in dict_loaded.items():
                    class_name = value.pop("__class__")
                    # Why don't we make use of an associative array instead
                    class_ = self.__class_dict[class_name]
                    obj = class_(**value)
                    self.__objects[key] = obj
        except (FileExistsError, FileNotFoundError):
            pass
