#!/usr/bin/env python3
# @brief This python script will exploit a custom backdoor placed in on a
#       website endpoint.
import traceback  # Exception stack trace
import readline  # command history and other features
from Exceptions import *
from LocalCommandProcessor import LocalCommandProcessor

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
