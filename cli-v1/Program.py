# CLI V1
# Program.py
# Like testing file. 
# Shows how to use the cli.

from CLIHandler import CLIHandler

def main():
    CLI = CLIHandler()
    CLI.Welcome()
    CLI.CommandLoop()
    CLI.Exit()

if __name__ == "__main__":
    main()