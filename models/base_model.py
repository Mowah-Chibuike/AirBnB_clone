#!/usr/bin/python3

import uuid
from datetime import datetime

class BaseModel:

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __str__(self):
        return "[{}] ({}) {}".format(__class__.__name__, self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.now()
    
    def to_dict(self):
        dict = {}
        for key in self.__dict__.keys():
            if type(self.__dict__[key]) is datetime:
                dict[key] = self.__dict__[key].isoformat()
            else:
                dict[key] = self.__dict__[key]
            dict["__class__"] = __class__.__name__
        return dict



my_model = BaseModel()
my_model.name = "My First Model"
my_model.my_number = 89
print(my_model)
my_model.save()
print(my_model)
my_model_json = my_model.to_dict()
print(my_model_json)
print("JSON of my_model:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))