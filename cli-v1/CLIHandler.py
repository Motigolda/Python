from Commands import Commands
from Strings import Strings
import os

class CLIHandler:
    
    def __init__(self):
        self.commands = Commands()

    def Welcome(self, clear = None):
        if clear or clear is None:
            self.ClearScreen()
        print(Strings.cli["welcome"])

    def WaitForCommand(self, clear = None):
        if clear:
            self.ClearScreen()

        command = input(Strings.cli["commandWait"])

        if len(command) > 0:
            success = Commands.Run(self.commands, command)
        else:
            return None

        if success == Commands.codes["exit"]:
            return Commands.codes["exit"]
        
        elif not success:
            print(Strings.commands['invalid'])
        
        elif success == Commands.codes['clear']:
            self.ClearScreen()
            
        return Commands.codes["valid"]

    def CommandLoop(self):
        while self.WaitForCommand() != Commands.codes["exit"]:
            pass

    def ClearScreen(self):
        os.system('cls')

    def Exit(self, clear = None):
        if clear or clear is None:
            self.ClearScreen()

        print(Strings.cli["exit"])
        os.system('pause')


def main():
    CLI = CLIHandler()
    CLI.Welcome(clear = True)
    CLI.CommandLoop()
    CLI.Exit(clear = True)

if __name__ == "__main__":
    main()
    