import traceback

class ExitException(Exception):
    pass

class NXCommand(Exception):
    pass

class CommandProcessor():
    def __init__(self):
        self.commands = {
            "help": self.__help,
            "exit": self.__exit
        }

    def __help(self, options):
        print("Help menu:")

    def __exit(self, options):
        raise ExitException()   

    def process_command(self, command: str):
        split = command.split(" ", 2)
        base = split[0]

        options = ""
        if len(split) > 1:
            options = split[1]
        
        if base in self.commands:
            self.commands[base](options)
        else:
            raise NXCommand()

        


if __name__ == "__main__":
    processor = CommandProcessor()
    try:
        print("Welcome to ASPLOIT.")
        print("For help, type 'help'")
        while (True):
            command = input("> ")
            try:
                processor.process_command(command)
            except NXCommand:
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

