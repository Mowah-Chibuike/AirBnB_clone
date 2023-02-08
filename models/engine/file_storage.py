#!/usr/bin/python3
"""
Module contains the FileStorage class
"""
import json


class FileStorage:
    """
    FileStorage Class
    """

    __file_path = "./file.json"
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
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj.to_dict()

    def save(self):
        """
        serializes __objects to the JSON file
        """
        with open(self.__file_path, mode='w+', encoding='utf-8') as file:
            json.dump(self.__objects, file)

    def reload(self):
        """
        deserializes the JSON file to __objects (only if the JSON file \
        (__file_path) exists ; otherwise, do nothing. If the file doesn’t\
        exist, no exception should be raised
        """
        try:
            with open(self.__file_path, mode='r', encoding='utf-8') as file:
                file.seek(0, 0)
                dict_to_load = json.load(file)
                self.__objects = dict_to_load
        except (FileExistsError, FileNotFoundError):
            pass
