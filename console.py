#!/usr/bin/python3
"""
Module contains the HBNBCommand class
"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
import json


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter for the HBNB console
    """
    prompt = "(hbnb) "
    # Stored all supported classes in an associative array i.e dictionary
    __class_dict = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
    }
    # Stored all objects from storage
    __objects = storage.all()

    def emptyline(self):
        pass

    def do_create(self, clsname):
        """
Creates a new instance of BaseModel, saves it (to the JSON file) and prints \
the id
        """
        if not clsname:
            print("** class name missing **")
        elif clsname not in self.__class_dict:
            print("** class doesn't exist **")
        else:
            # get the class from the associative array
            new = self.__class_dict[clsname]()
            new.save()
            print(new.id)

    def do_show(self, inst_attr):
        """
Prints the string representation of an instance based on the class name and \
id
        """
        if not inst_attr:
            print("** class name missing **")
        else:
            # splitted the arguments based on the space character
            args = inst_attr.split()
            if args[0] not in self.__class_dict:
                print("** class doesn't exist **")
                return
            if len(args) < 2:
                print("** instance id missing **")
                return
            # recreate the key from the arguments passed
            key = "{}.{}".format(args[0], args[1])
            if key in self.__objects:
                value = self.__objects[key]
                print(value)
            else:
                print("** no instance found **")

    def do_destroy(self, obj):
        """
Deletes an instance based on the class name and id
        """
        if not obj:
            print("** class name missing **")
        else:
            args = obj.split()
            if args[0] not in self.__class_dict:
                print("** class doesn't exist **")
                return
            if len(args) < 2:
                print("** instance id missing **")
                return
            key = "{}.{}".format(args[0], args[1])
            if key in self.__objects:
                del (self.__objects[key])
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, clsname):
        """
Prints all string representation of all instances based or not on the class \
name.
        """
        obj_list = []
        if not clsname:
            for value in self.__objects.values():
                obj_list.append(str(value))
            print(obj_list)
        elif clsname not in self.__class_dict:
            print("** class doesn't exist **")
        else:
            for key, value in self.__objects.items():
                if key.startswith(clsname):
                    obj_list.append(str(value))
            print(obj_list)

    def do_update(self, param):
        """
Updates an instance based on the class name and id by adding or updating \
attribute
        """
        if not param:
            print("** class name missing **")
        else:
            # split params based on the double quote character (")
            args = param.split('"')
            # then split the first element of the list based on space
            inner = args.pop(0).split()
            # Reinsert them in their correct positions
            for idx, item in enumerate(inner):
                args.insert(idx, item)
            len_args = len(args)
            if args[0] not in self.__class_dict:
                print("** class doesn't exist **")
                return
            if len_args < 2:
                print("** instance id missing **")
                return
            key = "{}.{}".format(args[0], args[1])
            if key in self.__objects:
                if len_args < 3:
                    print("** attribute name missing **")
                    return
                if len_args < 4:
                    print("** value missing **")
                    return
                obj = self.__objects[key]
                # check if it's a numeric value and convert it to an integer
                if args[3].isdigit():
                    value = int(args[3])
                # check if it is a float and convert it to a float
                else:
                    try:
                        value = float(args[3])
                    except (ValueError, TypeError):
                        value = args[3]
                obj.__dict__[args[2]] = value
                obj.save()
            else:
                print("** no instance found **")

    def do_User(self, line):
        """
Handles all specific User commands
        """
        if not line.endswith(")") \
                and line.count(")") != 1 and line.count(")") != 1:
            return cmd.Cmd.default(self, "User" + line)
        args_list = parse(line)
        if line == ".all()":
            return cmd.Cmd.onecmd(self, "all User")
        if line == ".count()":
            count = 0
            for key in self.__objects.keys():
                if key.startswith("User"):
                    count += 1
            print(count)
        elif args_list[0] == "show":
            return cmd.Cmd.onecmd(self, "show User " + args_list[1].strip('"'))
        elif args_list[0] == "destroy":
            return cmd.Cmd.onecmd(
                self, "destroy User " + args_list[1].strip('"'))
        elif args_list[0] == "update":
            try:
                args = args_list[1].split(", ", 1)
                user_id = args[0].strip('"')
                key = "User." + user_id
                if key not in self.__objects and user_id:
                    print("** no instance found **")
                    return
                update_dict = json.loads(args[1].replace("'", '"'))
                for key, value in update_dict.items():
                    cmd.Cmd.onecmd(
                        self, 'update User {} {} "{}"'.format(
                            user_id, key, value))
            except Exception:
                args_str = ""
                args = args_list[1].split(", ")
                for idx, token in enumerate(args):
                    if idx != 0:
                        args_str += " "
                    if idx == 0 or idx == 1:
                        args_str += token.strip('"')
                    else:
                        args_str += token
                return cmd.Cmd.onecmd(self, "update User " + args_str)
        else:
            return cmd.Cmd.default(self, "User" + line)

    def do_State(self, line):
        """
Handles specific State commands
        """
        if not line.endswith(")") \
                and line.count(")") != 1 and line.count(")") != 1:
            return cmd.Cmd.default(self, "State" + line)
        args_list = parse(line)
        if line == ".all()":
            return cmd.Cmd.onecmd(self, "all State")
        if line == ".count()":
            count = 0
            for key in self.__objects.keys():
                if key.startswith("State"):
                    count += 1
            print(count)
        elif args_list[0] == "show":
            return cmd.Cmd.onecmd(
                self, "show State " + args_list[1].strip('"'))
        elif args_list[0] == "destroy":
            return cmd.Cmd.onecmd(
                self, "destroy State " + args_list[1].strip('"'))
        elif args_list[0] == "update":
            try:
                args = args_list[1].split(", ", 1)
                user_id = args[0].strip('"')
                key = "State." + state_id
                if key not in self.__objects and user_id:
                    print("** no instance found **")
                    return
                update_dict = json.loads(args[1].replace("'", '"'))
                for key, value in update_dict.items():
                    cmd.Cmd.onecmd(
                        self, 'update State {} {} "{}"'.format(
                            user_id, key, value))
            except Exception:
                args_str = ""
                args = args_list[1].split(", ")
                for idx, token in enumerate(args):
                    if idx != 0:
                        args_str += " "
                    if idx == 0 or idx == 1:
                        args_str += token.strip('"')
                    else:
                        args_str += token
                    return cmd.Cmd.onecmd(self, "update State " + args_str)
        else:
            return cmd.Cmd.default(self, "State" + line)

    def do_BaseModel(self, line):
        """
        """
        if not line.endswith(")") \
                and line.count(")") != 1 and line.count(")") != 1:
            return cmd.Cmd.default(self, "BaseModel" + line)
        args_list = parse(line)
        if line == ".all()":
            return cmd.Cmd.onecmd(self, "all BaseModel")
        if line == ".count()":
            count = 0
            for key in self.__objects.keys():
                if key.startswith("BaseModel"):
                    count += 1
            print(count)
        elif args_list[0] == "show":
            return cmd.Cmd.onecmd(
                self, "show BaseModel " + args_list[1].strip('"'))
        elif args_list[0] == "destroy":
            return cmd.Cmd.onecmd(
                self, "destroy BaseModel " + args_list[1].strip('"'))
        elif args_list[0] == "update":
            try:
                args = args_list[1].split(", ", 1)
                user_id = args[0].strip('"')
                key = "BaseModel." + user_id
                if key not in self.__objects and user_id:
                    print("** no instance found **")
                    return
                update_dict = json.loads(args[1].replace("'", '"'))
                for key, value in update_dict.items():
                    cmd.Cmd.onecmd(
                        self, 'update BaseModel {} {} "{}"'.format(
                            user_id, key, value))
            except Exception:
                args_str = ""
                args = args_list[1].split(", ")
                for idx, token in enumerate(args):
                    if idx != 0:
                        args_str += " "
                    if idx == 0 or idx == 1:
                        args_str += token.strip('"')
                    else:
                        args_str += token
                return cmd.Cmd.onecmd(self, "update BaseModel " + args_str)
        else:
            return cmd.Cmd.default(self, "BaseModel" + line)

    def do_quit(self, s):
        """

Quit command to exit the program
        """
        return True

    def do_EOF(self, s):
        """
Intepretes the Ctrl + D shortcut(EOF) command
        """
        print()
        return True


def parse(args):
    """
    Converts a string to a command for the onecmd method of the cmd module \
to execute
    """
    args_str = args.strip(".").strip(")")
    return args_str.split("(")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
