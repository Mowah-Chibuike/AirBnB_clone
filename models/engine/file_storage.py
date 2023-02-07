#!/usr/bin/python3
"""
Module contains the FileStorage class
"""
import json

class FileStorage:
    """
    FileStorage Class
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Return __objects
        """
        return self.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        self.__objects["{}.{}".format(type(obj), obj.id)] = obj

    def save(self):
        """
        serializes __objects to the JSON file
        """
        with open(self.__file_path, mode='w') as file:
            json_data = json.dumps(self.__objects)
            file.write(json_data)

    def reload(self):
        """
        deserializes the JSON file to __objects
        """
        try:
            with open(self.__file_path, mode='r') as file:
                self.__objects = json.load(file)
        except FileExistsError:
            pass