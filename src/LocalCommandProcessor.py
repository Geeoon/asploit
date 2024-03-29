import importlib.util  # dynamic import
import inspect  # dynamic import
from pathlib import Path  # dynamic import
from Exceptions import *
from CommandProcessor import CommandProcessor
from ExploitProcessor import ExploitProcessor
from PHPExploitProcessor import PHPExploitProcessor
from NodeExploitProcessor import NodeExploitProcessor
from FlaskExploitProcessor import FlaskExploitProcessor
from ASPClassicExploitProcessor import ASPClassicExploitProcessor
from BotnetCommandProcessor import BotnetCommandProcessor

"""
@brief The LocalCommandProcessor class is a class that accepts commands before
        exploitation. It is used to set up the environment and exploit
        variables.
        Inherits from the CommandProcessor class.
"""
class LocalCommandProcessor(CommandProcessor):
    def __init__(self):
        self.exploitClasses = [ASPClassicExploitProcessor,
                               FlaskExploitProcessor,
                               NodeExploitProcessor,
                               PHPExploitProcessor]
        self.exploit: ExploitProcessor = None
        
        super().__init__()
        self.commands["exploit"] = { 
                "method": self.__exploit,
                "description": ("Start the exploit, "
                    "given the preconditions are met."),
                "usage": "exploit"
            }
        
        self.commands["set"] = {
                "method": self.__set,
                "description": "Set or display exploit variables.",
                "usage": ("set variable [value]\n"
                          "    variable: variable to set.\n"
                          "    value: value to set variable to.")
            }

        self.commands["loadext"] = {
                "method": self.__loadext,
                "description": "Load an extension.",
                "usage": ("loadext path\n"
                          "    path: path to the extension.")
        }

        self.commands["botnet"] = {
                "method": self.__botnet,
                "description": "Switch to botnet mode.",
                "usage": "botnet"
        }
            
        # exploit variables
        self.variables = {
            "TARGET_HOST": {"value": "localhost:8000", "required": True},
            "TARGET_PATH": {"value": "/", "required": True},
            "TARGET_TYPE": {"value": "PHP", "required": True},
            "METHOD": {"value": "GET", "required": True},
            "HEADER": {"value": "EXPLOIT", "required": True}
        }

    """
    @brief See base class for details.
    """
    def _Base__get_prefix(self):
        if self.exploit:
            return self.exploit._Base__get_prefix()
        return super()._Base__get_prefix()
        
    """
    @brief exploit the target machine.
    @param options Not used.
    @pre the TARGET_TYPE is a valid target type.
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
        
        for exploitClass in self.exploitClasses:
            if (self.variables['TARGET_TYPE']['value'].upper()
                                  == exploitClass.get_name().upper()):
                self.exploit = (exploitClass(
                                    self.variables['TARGET_HOST']['value'],
                                    self.variables['TARGET_PATH']['value'],
                                    self.variables['METHOD']['value'],
                                    self.variables['HEADER']['value']))
                return
        raise CommandException("TARGET_TYPE is not supported.")

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
    @brief Loan an external extension (an exploit processor).
    @param options the path to the extension.
    @throw ExtensionException if the extension couldn't be loaded properly.
    """
    def __loadext(self, options: str):
        try:
            modulePath = Path(options)
            spec = importlib.util.spec_from_file_location(
                    modulePath.stem,
                    modulePath.resolve())
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, ExploitProcessor) and 
                    name != "ExploitProcessor"):
                    for exploit in self.exploitClasses:
                        if exploit.get_name() == obj.get_name():
                            raise ExtensionException(
                                "Already loaded extension of same type.")
                    self.exploitClasses.append(obj)
        except (CommandException, ExtensionException) as e:
            raise e
        except Exception:
            raise ExtensionException("Couldn't load extension, check the path.")
        pass

    def __botnet(self, options: str):
        print("Switching to botnet mode...")
        self.exploit = BotnetCommandProcessor(self.exploitClasses)

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
        else:
            super().process_command(command)
