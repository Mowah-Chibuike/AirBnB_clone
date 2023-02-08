#!/usr/bin/python3
"""
Module contains the HBNBCommand class
"""
import cmd


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter for the HBNB console
    """
    prompt = "(hbnb) "

    def emptyline(self):
        pass

    def do_quit(self, s):
        """
        Quits the command intepreter
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
