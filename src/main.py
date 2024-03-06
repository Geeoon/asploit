#!/usr/bin/env python3
# @brief This python script will exploit a custom backdoor placed in on a
#       website endpoint.
import os
import traceback

# @brief Exception raised to exit program.
class ExitException(Exception):
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
            "help": { 
                "method": self.__help,
                "description": "Display the help screen."
            },
            "exit": {
                "method": self.__exit,
                "description": "Exit the program."
            },
            "exploit": { 
                "method": self.__exploit,
                "description": ("Start the exploit, "
                    "given the preconditions are met.")
            },
            "clear": {
                "method": self.__clear,
                "description": "Clear the screen."
            },
            "set": {
                "method": self.__set,
                "description": "Set or display exploit variables."
            }
        }

        # exploit variables
        self.variables = {
            "TARGET": "",
            "TARGET_TYPE": "ASP"
        }

        # have we successfully exploited yet?
        self.post = False

    """
    @brief Help command that prints commands and their usage.
    @param options The specific command to display help for.
    """
    def __help(self, options: str):
        # if no command is specified
        if len(options) == 0:
            for command in self.commands:
                print((f"    {'{0: <10}'.format(command)}"
                       f" {self.commands[command]['description']}"))
        else:  # look up specific command
            if options in self.commands:
                print(f"    {options}: {self.commands[options]['description']}")
            else:  # command does not exist
                raise CommandException(f"    '{options}' command not found.")

    """
    @brief Command to exit the program or the exploit shell.
    @throw ExitException to exit the program.
    @param options Not used.
    """
    def __exit(self, options: str):
        if self.post:
            # exit shell
            self.post = False
            print("Exiting exploit shell.")
        else:
            # exit program
            raise ExitException()
    
    """
    @brief Command to clear the screen.
    @param options Not used.
    """
    def __exploit(self, options: str):
        print("Attempting to exploit target at ")
        self.post = True

    """
    @brief Command to set exploit variables.
    @param the variable to be set and the value, if any.
    @throw CommandException if the variable does not exist, or if the vlaue is
            invalid.
    """
    def __set(self, options: str):
        if os.name == 'nt':  # Windows
            os.system("cls")
        else:  # POSIX
            os.system("clear")

    """
    @brief Command to set exploit variables.
    @param the variable to be set and the value, if any.
    @throw CommandException if the variable does not exist, or if the vlaue is
            invalid.
    """
    def __clear(self, options: str):
        if os.name == 'nt':  # Windows
            os.system("cls")
        else:  # POSIX
            os.system("clear")

    """
    @brief Command to set and display exploit variables.
    @param the variable to be set and the value, if any.
    @throw CommandException if the variable does not exist, or if the value is
            invalid.
    """
    def __set(self, options: str):
        if len(options) == 0:  # list all variables
            print(f"{'{0: <20}'.format(f'VARIABLE')} VALUE")
            for var in self.variables:
                print(f"{'{0: <20}'.format(var)} {self.variables[var]}")
        else:
            split = options.split(" ", 1)
            var = split[0]
            if var in self.variables:
                value = ""
                if len(split) > 1:
                    value = split[1]
                self.variables[var] = value
                print(f"'{var}' set to '{value}'")
            else:
                raise CommandException(f"'{var}' is not a variable.")

    """
    @brief Processes a command string.
    @param command A string representing the whole command to be processed.
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
    
    """
    @brief Getter for exploit status (True or False)
    @return bool for if we are in the exploit shell.
    """
    def expliot_status(self):
        return self.post

if __name__ == "__main__":
    processor = CommandProcessor()
    try:
        print("Welcome to ASPLOIT.")
        print("For help, type 'help'")
        while (True):
            pre = ">"
            if processor.expliot_status():
                pre = "shell>"
            command = input(pre)
            try:
                processor.process_command(command)
            except CommandException as e:
                print(str(e))
    except ExitException:
        print("Exiting...")
    except KeyboardInterrupt:
        print()
        print("Keyboard Interrupt")
    except Exception:
        print("Unrecoverable Exception: ")
        print(traceback.format_exc())
    finally:
        print("Goodbye.")

