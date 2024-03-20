from Exceptions import *
from CommandProcessor import CommandProcessor
"""
@brief The BotnetCommandProcessor class is a class that accepts commands to be
        executed on a botnet. It is used to set up the environment and exploit
        variables for a botnet while also executing commands on the entire
        botnet.
        Inherits from the CommandProcessor class.
"""
class BotnetCommandProcessor(CommandProcessor):
    def __init__(self):
        self.targets = []
        super().__init__()
        self.commands["add"] = {
                "method": self.__add,
                "description": "Add a target to the list of targets.",
                "usage": ("add name host path type method header\n"
                          "    name: the name of the target.\n"
                          "    host: the hostname of the target.\n"
                          "    path: the path of the backdoor on the target.\n"
                          "    type: the type of backdoor on the target.\n"
                          "    method: the HTTP method for the backdoor.\n"
                          "    header: the HTTP header to communicate over.")
            }
        self.commands["list"] = {
                "method": self.__list,
                "description": "List all the targets.",
                "usage": ("list")
        }
        
    """
    @brief Add a target to the list of targets.
    @throw CommandException if host is malformatted.
    """
    def __add(self, options: str):
        if options.count(" ") != 5:
            raise CommandException("Incorrect usage. "
                                   "Run 'help add' for usage.")
        name, host, path, target_type, method, header = options.split(" ")
        if name in map(lambda host : host["name"], self.targets):
            raise CommandException("Name already in list.")
        self.targets.append({
            "name": name,
            "host": host,
            "path": path,
            "type": target_type,
            "method": method,
            "header": header
        })

    """
    @brief List all of the hosts
    """
    def __list(self, options: str):
        if len(self.targets) == 0:
            raise CommandException("No hosts added.")

        print(self.targets[0]["name"])
        print(f"{self.targets[0]['host']}{self.targets[0]['path']}")
        print(self.targets[0]["type"])
        print(self.targets[0]["header"])
        for target in self.targets[1:]:
            print("-" * 80)
            print(target["name"])
            print(f"{target['host']}{target['path']}")
            print(target["type"])
            print(target["header"])

    """
    @brief See base class for details.
    """
    def _Base__get_prefix(self):
        return "botnet > "
    