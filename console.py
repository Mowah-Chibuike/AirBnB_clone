#!/usr/bin/python3
"""
Module contains the HBNBCommand class
"""
import cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter for the HBNB console
    """
    prompt = "(hbnb) "
    __class_dict = {'BaseModel': BaseModel}

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
            args = inst_attr.split()
            if args[0] not in self.__class_dict:
                print("** class doesn't exist **")
                return
            if len(args) < 2:
                print("** instance id missing **")
                return
            key = "{}.{}".format(args[0], args[1])
            if key in storage.all():
                value = storage.all()[key]
                cls_of_inst = self.__class_dict[value["__class__"]]
                print(cls_of_inst(**value))
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
            if key in storage.all():
                del (storage.all()[key])
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
            for value in storage.all().values():
                cls_of_inst = self.__class_dict[value["__class__"]]
                new = cls_of_inst(**value)
                obj_list.append(str(new))
            print(obj_list)
        elif clsname not in self.__class_dict:
            print("** class doesn't exist **")
        else:
            for key, value in storage.all().items():
                if key.startswith(clsname):
                    cls_of_inst = self.__class_dict[value["__class__"]]
                    new = cls_of_inst(**value)
                    obj_list.append(str(new))
            print(obj_list)

    def do_update(self, param):
        """
Updates an instance based on the class name and id by adding or updating \
attribute 
        """
        if not param:
            print("** class name missing **")
        else:
            args = param.split('"')
            inner = args.pop(0).split()
            for idx, item in enumerate(inner):
                args.insert(idx, item)
            if args[0] not in self.__class_dict:
                print("** class doesn't exist **")
                return
            if len(args) < 2:
                print("** instance id missing **")
                return
            key = "{}.{}".format(args[0], args[1])
            if key in storage.all():
                if len(args) < 3:
                    print("** attribute name missing **")
                    return
                if len(args) < 4:
                    print("** value missing **")
                obj_dict = storage.all()[key]
                if args[3].isnumeric():
                    value = int(args[3])
                elif "." in args[3]:
                    to_validate = ""
                    for item in args[3].split("."):
                        to_validate += item
                    if to_validate.isnumeric():
                        value = float(args[3])
                else:
                    value = args[3]
                obj_dict[args[2]] = value
                storage.save()
            else:
                print("** no instance found **")

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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
