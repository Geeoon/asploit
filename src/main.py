#!/usr/bin/env python3
# @brief This python script will exploit a custom backdoor placed in on a website endpoint.

import traceback

# @brief Exception raised to exit program.
class ExitException(Exception):
    pass

# @brief Exception raised for non-existant commands.
class NoCommand(Exception):
    pass

# @brief Exception raised for command errors. Must be raised with a message.
class CommandException(Exception):
    pass

"""
@brief The CommandProcessor class accepts commands passed into it and processes
        it appropriately.
"""
class CommandProcessor():
    """
    @brief constructs/initalizes a CommandProcessor instance.
    """
    def __init__(self):
        self.commands = {
            "help": { "method": self.__help, "description": "Display the help screen" },
            "exit": { "method": self.__exit, "description": "Exit the program" },
            "exploit": { 
                "method": self.__exploit,
                "description": "Start the exploit, given the preconditions are met."
            }
        }
        self.target = ""
        self.target_type = "ASP"

    """
    @brief Simple help command that prints options and their usage.
    @param options Not used.
    """
    def __help(self, options: str):
        print("Help:")

    """
    @brief Simple exit command that throws an ExitException.
    @param options Not used.
    """
    def __exit(self, options: str):
        raise ExitException()
    
    """
    @brief Command to exploit the target.
    @param options Not used.
    @pre the TARGET field has been set and is a backdoored endpoint.
    @pre the TARGET_TYPE field has been set and is a valid TARGET_TYPE.
    @throw CommandException if the precondtions are not met.
    """
    def __exploit(self, options: str):
        print("Attempting to exploit target at ")

    """
    @brief Processes a command string.
    @param command A string representing the whole command to be processed.
    @pre \p command is a valid command to be ran.
    @pre \p command has its preconditions met. 
    @throw NoCommand if the command doesn't exist.
    """
    def process_command(self, command: str):
        split = command.split(" ", 2)
        base = split[0]

        options = ""
        if len(split) > 1:
            options = split[1]
        
        if base in self.commands:
            self.commands[base](options)
        else:
            raise NoCommand()

if __name__ == "__main__":
    processor = CommandProcessor()
    try:
        print("Welcome to ASPLOIT.")
        print("For help, type 'help'")
        while (True):
            command = input("> ")
            try:
                processor.process_command(command)
            except NoCommand:
                print(f"Couldn't find '{command.split(' ', 2)[0]}' command.")
    except ExitException:
        print("Exiting...")
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    except Exception:
        print("Unrecoverable Exception: ")
        print(traceback.format_exc())
    finally:
        print("Goodbye.")

