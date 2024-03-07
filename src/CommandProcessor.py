import os  # system calls
from Exceptions import *

"""
@brief The CommandProcessor class accepts commands passed into it and processes
        it appropriately. Acts as base class for all shells.
"""
class CommandProcessor():
    """
    @brief constructs/initalizes a CommandProcessor instance.
    """
    def __init__(self):
        self.commands = {
            "help": { 
                "method": self._Base__help,
                "description": "Display the help screen."
            },
            "clear": {
                "method": self._Base__clear,
                "description": "Clear the screen."
            },
            "exit": {
                "method": self.__exit,
                "description": "Exit the program or exploit."
            }
        }

    """
    @brief Help command that prints commands and their usage.
    @param options The specific command to display help for.
    @pre \p options is specify a valid command, or nothing.
    @throw CommandException if the pre-condition is not met.
    """
    def _Base__help(self, options: str):
        # if no command is specified
        if len(options) == 0:
            for command in self.commands:
                print((f"    {'{0: <10}'.format(command)}"
                       f" {self.commands[command]['description']}"))
        else:  # look up specific command
            if options in self.commands:
                print((f"    "
                      f"{options}: {self.commands[options]['description']}"))
            else:  # command does not exist
                raise CommandException(f"    '{options}' command not found.")

    """
    @brief Command to clear screen.
    @param options Not used.
    """
    def _Base__clear(self, options: str):
        if os.name == 'nt':  # Windows
            os.system("cls")
        else:  # POSIX
            os.system("clear")

    """
    @brief Command to exit the program or the exploit shell.
    @param options Not used.
    @throw ExitException to exit the program.
    """
    def __exit(self, options: str):
        # exit shell
        raise ExitException()

    """
    @brief Processes a command string.
    @param command a string representing the whole command to be processed.
    @pre \p command is a valid command to be ran.
    @pre \p command has its preconditions met. 
    @throw CommandException if the command doesn't exist.
    """
    def process_command(self, command: str):
        split = command.split(" ", 1)
        base = split[0]

        options = ""
        if len(split) > 1:
            options = split[1]
        
        if base in self.commands:
            self.commands[base]["method"](options)
        else:
            raise CommandException(
                f"'{command.split(' ', 1)[0]}' command not found.")
