#!/usr/bin/python3
'''
HBNBCommand:
    the entry point of the command interpreter.
'''
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    '''The entry point of the command interpreter.

    Attributes:
        prompt (str): the command prompt.
        __classes (dict): dictionary contains all classes.
    '''
    __classes = {'BaseModel': BaseModel, 'User': User, 'State': State,
                 'City': City, 'Amenity': Amenity,
                 'Place': Place, 'Review': Review}
    prompt = '(hbnb) '

    def do_quit(self, _):
        '''Exit the program with 'quit' command'''
        return True

    def do_EOF(self, _):
        '''Exit the program with 'EOF' signal'''
        print('')
        return True

    def emptyline(self):
        '''Don't execute anything'''

    def do_create(self, arg):
        '''Creates a new instance of class, saves it
        (to the JSON file) and prints the id
        '''
        inputs = arg.split()
        is_valid = self.validate_input(inputs, ['classname'])

        if not is_valid:
            return

        obj = self.__classes[inputs[0]]()
        obj.save()
        print(obj.id)

    def do_update(self, arg):
        '''Updates an instance based on the class name and id by adding
        or updating attribute and save the change into the JSON file.
        '''
        inputs = arg.split()
        is_valid = self.validate_input(
            inputs, ['classname', 'id', 'attribute_name', 'attribute_value'])

        if not is_valid:
            return

        objects = storage.all()
        k = '{}.{}'.format(inputs[0], inputs[1])
        obj = objects.get(k)

        setattr(obj, inputs[2], inputs[3])

        storage.save()

    def do_show(self, arg):
        '''Prints the string representation of an instance
        based on the class name and id.
        '''
        inputs = arg.split()
        is_valid = self.validate_input(inputs, ['classname', 'id'])

        if not is_valid:
            return

        objects = storage.all()
        k = '{}.{}'.format(inputs[0], inputs[1])

        obj = objects.get(k, None)

        print(obj)

    def do_destroy(self, arg):
        '''Deletes an instance based on the class name and id
        and save the change into the JSON file
        '''
        inputs = arg.split()
        is_valid = self.validate_input(inputs, ['classname', 'id'])

        if not is_valid:
            return

        objects = storage.all()
        k = '{}.{}'.format(inputs[0], inputs[1])

        del objects[k]
        storage.save()

    def do_all(self, arg):
        '''Prints all string representation of all instances
        based or not on the class name.
        '''
        inputs = arg.split()
        objects = storage.all()

        res = []
        if len(inputs) < 1:
            for _, v in objects.items():
                res.append(str(v))
            print(res)
            return

        classname = inputs[0]
        if classname not in self.__classes:
            print("** class doesn't exist **")
            return

        for _, v in objects.items():
            if v.__class__.__name__ == classname:
                res.append(str(v))
        print(res)

    def do_count(self, arg):
        '''Retrieve the number of instances of a class.
        '''
        counter = 0
        objects = storage.all()
        for _, v in objects.items():
            if v.__class__.__name__ == arg:
                counter += 1
        print(counter)

    def default(self, line):
        args = line.split('.')
        classes = self.__classes

        if len(args) != 2:
            super().default(line)
            return

        classname = args[0]
        if classname not in classes:
            super().default(line)
            return

        method = args[1].split('(')[0]
        if method == 'count':
            self.do_count(classname)

        if method == 'destroy':
            obj_id = args[1].split('(')[1].split(')')[0]
            self.do_destroy('{} {}'.format(classname, obj_id))

    def validate_input(self, inputs, args):
        '''Validate user input

        Args:
            inp (str): user input.
            args (list): the args to be checked against input.
        '''
        classes = self.__classes

        for i, arg in enumerate(args):
            if arg == 'classname':
                if len(inputs) == 0 or i > len(inputs):
                    print('** class name missing **')
                    return False
                if inputs[i] not in classes:
                    print('** class doesn\'t exist **')
                    return False

            if arg == 'id':
                if i > len(inputs) - 1:
                    print('** instance id missing **')
                    return False

                objects = storage.all()
                k = '{}.{}'.format(inputs[0], inputs[1])

                obj = objects.get(k, None)
                if obj is None:
                    print('** no instance found **')
                    return False

            if arg == 'attribute_name':
                if i > len(inputs) - 1:
                    print('** attribute name missing **')
                    return False

            if arg == 'attribute_value':
                if i > len(inputs) - 1:
                    print('** value missing **')
                    return False

        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
