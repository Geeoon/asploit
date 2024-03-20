# @brief Exception raised to exit program.
class ExitException(Exception):
    pass

# @brief Exception raised for command errors. Must be raised with a message.
class CommandException(Exception):
    pass

# @brief Exception raised for exception loading errors. Must be raised with a message.
class ExtensionException(Exception):
    pass