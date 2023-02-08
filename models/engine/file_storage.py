#!/usr/bin/python3
"""
Module contains the FileStorage class
"""
import json
#from models.base_model import BaseModel

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
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        serializes __objects to the JSON file
        """
        with open(self.__file_path, mode='w') as file:
            objects_to_save = {}
            for key, obj in self.__objects.items():
                objects_to_save[key] = obj.to_dict()
            json_data = json.dumps(objects_to_save)
            file.write(json_data)

    def reload(self):
        """
        deserializes the JSON file to __objects (only if the JSON file \
        (__file_path) exists ; otherwise, do nothing. If the file doesn’t\
        exist, no exception should be raised
        """
        try:
            with open(self.__file_path, mode='r') as file:
                dict_to_load = json.load(file)
                for key, value in dict_to_load.items():
                    class_name = value.pop("__class__")
                    class_ = globals()[class_name]
                    obj = class_(**value)
                    self.__objects[{key}] = obj
        except (FileExistsError, FileNotFoundError):
            pass

print(globals())
