# @brief Exception raised to exit program.
class ExitException(Exception):
    pass

# @brief Exception raised for command errors. Must be raised with a message.
class CommandException(Exception):
    pass