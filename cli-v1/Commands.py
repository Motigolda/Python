# CLI V1
# Commands.py
# This file is the core of your project
# You need to import your porject as package to this file,
# so you can use all it classes and functions. 
# Altough the main file is Program, the connection between your project and the user happens here.
# Here you call your function and write output for the user.

import Strings

class Commands:
    codes = {   "invalid":False,
                "valid":True,
                "exit":-1,
                "clear": -2}
    @staticmethod
    def Run(ins, raw_command = None):
        if raw_command is None:
            return

        command = getattr(ins, raw_command.split()[0], Commands.codes["invalid"])

        if command == Commands.codes["invalid"]:
            return False

        if len(raw_command.split()) > 1:
            args = raw_command.split()[1:]
            return command(args)

        return command()

    # Define here all your commands for cli
    # For example, help function:

    def help(self):
        method_list = [func for func in dir(Commands) if callable(getattr(Commands, func)) and not func.startswith("__") and not func.startswith("Run")]
        print("The available commands are:\n\n\t", end="")
        print(*method_list, sep="\n\t")
        return Commands.codes['valid']

    # Example command
    def minus1(self, args = None):
        if args is not None:
            try:
                print(int(args[0]) - 1)
            except ValueError:
                print("This is not a number!")
        else:
            print("Usage: minus1 [number]")   

        return Commands.codes['valid']
                
    def clear(self, args = None):
        return Commands.codes['clear']

    # *** Dont change the return value of exit command. ***
    # *** You can enter any content but dont change the return. ***
    
    def exit(self):
        return Commands.codes["exit"]